from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"(?:^|[\s\"'])/(?:Users|home|tmp|var|private|mnt)/"),
    re.compile(r"[A-Za-z]:\\\\"),
)
SECRET_PATTERNS = (
    re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


@dataclass(frozen=True, order=True)
class Finding:
    rule_id: str
    path: str
    message: str
    fix: str
    severity: str = "error"

    def render(self) -> str:
        return f"{self.severity.upper()} {self.rule_id} {self.path}: {self.message} Fix: {self.fix}"


def load_yaml_text(text: str, source: str) -> Any:
    if yaml is not None:
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError(f"invalid YAML in {source}: {exc}") from exc
    completed = subprocess.run(
        [
            "ruby",
            "-ryaml",
            "-rjson",
            "-e",
            "puts JSON.generate(YAML.safe_load(STDIN.read, permitted_classes: [Date], aliases: false))",
        ],
        input=text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "Ruby Psych fallback is unavailable"
        raise ValueError(f"invalid YAML in {source}: {detail}")
    return json.loads(completed.stdout)


def load_yaml(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"file does not exist: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"file is not UTF-8: {path}") from exc
    return load_yaml_text(text, path.as_posix())


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file does not exist: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"file is not UTF-8: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"file does not exist: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"file is not UTF-8: {path}") from exc


def nested_get(data: Any, dotted_path: str) -> Any:
    current = data
    for key in dotted_path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def normalize_text(value: Any) -> str:
    if isinstance(value, str):
        return value.lower()
    if isinstance(value, dict):
        return " ".join(normalize_text(v) for v in value.values())
    if isinstance(value, (list, tuple, set)):
        return " ".join(normalize_text(v) for v in value)
    if value is None:
        return ""
    return str(value).lower()


def has_all_groups(text: str, groups: dict[str, tuple[str, ...]]) -> list[str]:
    lowered = text.lower()
    return [name for name, terms in groups.items() if not any(term in lowered for term in terms)]


def collect_repository_files(root: Path) -> list[Path]:
    ignored = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored for part in path.parts):
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.as_posix())


def scan_secrets_and_absolute_paths(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in collect_repository_files(root):
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(Finding(
                    "MANIFEST-SECRET-001",
                    relative,
                    "possible secret or credential material detected",
                    "remove the secret and use an external credential mechanism",
                ))
                break
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(text):
                findings.append(Finding(
                    "MANIFEST-PATH-003",
                    relative,
                    "local absolute path detected",
                    "replace it with a repository-relative path or a portable shell expression",
                ))
                break
    return findings


def print_findings(findings: Iterable[Finding]) -> int:
    ordered = sorted(findings)
    for finding in ordered:
        print(finding.render())
    errors = sum(1 for finding in ordered if finding.severity == "error")
    warnings = sum(1 for finding in ordered if finding.severity == "warning")
    print(f"SUMMARY errors={errors} warnings={warnings} findings={len(ordered)}")
    return 1 if errors else 0


def main_guard(func: Any) -> None:
    try:
        raise SystemExit(func())
    except KeyboardInterrupt:
        print("ERROR VAL-RUN-INTERRUPTED <runtime>: validation interrupted. Fix: run the command again.", file=sys.stderr)
        raise SystemExit(130)
