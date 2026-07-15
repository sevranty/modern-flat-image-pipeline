from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from validation_common import Finding, KEBAB_RE, SEMVER_RE, load_json, load_yaml, main_guard, print_findings, read_text, scan_secrets_and_absolute_paths


def load_yaml_from_text(text: str, path: Path) -> Any:
    import yaml
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter in {path}: {exc}") from exc


def parse_skill_frontmatter(path: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    findings: list[Finding] = []
    try:
        text = read_text(path)
    except ValueError as exc:
        return None, [Finding("MANIFEST-SKILL-001", path.as_posix(), str(exc), "restore the canonical SKILL.md")]
    if not text.startswith("---\n"):
        return None, [Finding("MANIFEST-SKILL-002", path.as_posix(), "SKILL.md does not start with YAML frontmatter", "add `name` and `description` frontmatter")]
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, [Finding("MANIFEST-SKILL-003", path.as_posix(), "SKILL.md frontmatter is not closed", "close the YAML frontmatter with `---`")]
    try:
        data = load_yaml_from_text(text[4:end], path)
    except ValueError as exc:
        return None, [Finding("MANIFEST-SKILL-004", path.as_posix(), str(exc), "fix the SKILL.md YAML frontmatter")]
    if not isinstance(data, dict):
        findings.append(Finding("MANIFEST-SKILL-005", path.as_posix(), "frontmatter must be a mapping", "define `name` and `description` keys"))
        return None, findings
    for key in ("name", "description"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            findings.append(Finding("MANIFEST-SKILL-006", path.as_posix(), f"missing non-empty frontmatter field `{key}`", f"add a non-empty `{key}` value"))
    return data, findings


def validate(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    skill_dir = root / "skills" / "modern-flat-image-pipeline"
    skill_path = skill_dir / "SKILL.md"
    agent_path = skill_dir / "agents" / "openai.yaml"

    try:
        manifest = load_json(manifest_path)
    except ValueError as exc:
        return [Finding("MANIFEST-JSON-001", manifest_path.relative_to(root).as_posix(), str(exc), "restore valid UTF-8 JSON")]
    if not isinstance(manifest, dict):
        return [Finding("MANIFEST-JSON-002", manifest_path.relative_to(root).as_posix(), "manifest top level must be an object", "use a JSON object")]

    name = manifest.get("name")
    if not isinstance(name, str) or not KEBAB_RE.fullmatch(name):
        findings.append(Finding("MANIFEST-NAME-001", ".codex-plugin/plugin.json", "plugin name must be kebab-case", "set `name` to `modern-flat-image-pipeline`"))
    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        findings.append(Finding("MANIFEST-VERSION-001", ".codex-plugin/plugin.json", "plugin version is not valid semantic versioning", "set a version such as `0.1.0`"))
    skills_path = manifest.get("skills")
    if not isinstance(skills_path, str) or not skills_path.startswith("./"):
        findings.append(Finding("MANIFEST-PATH-001", ".codex-plugin/plugin.json", "`skills` must be a relative path starting with `./`", "set `skills` to `./skills/`"))
    elif not (root / skills_path).exists():
        findings.append(Finding("MANIFEST-PATH-002", ".codex-plugin/plugin.json", f"manifest skills path does not exist: {skills_path}", "create the path or correct the manifest"))

    interface = manifest.get("interface")
    prompts = interface.get("defaultPrompt") if isinstance(interface, dict) else None
    if prompts is not None:
        if not isinstance(prompts, list) or len(prompts) > 3:
            findings.append(Finding("MANIFEST-PROMPT-001", ".codex-plugin/plugin.json", "`defaultPrompt` must contain at most three strings", "keep one to three short starter prompts"))
        elif any(not isinstance(prompt, str) or len(prompt) > 128 for prompt in prompts):
            findings.append(Finding("MANIFEST-PROMPT-002", ".codex-plugin/plugin.json", "each starter prompt must be a string no longer than 128 characters", "shorten every starter prompt"))

    frontmatter, frontmatter_findings = parse_skill_frontmatter(skill_path)
    findings.extend(frontmatter_findings)
    if frontmatter and isinstance(name, str) and frontmatter.get("name") != name:
        findings.append(Finding("MANIFEST-NAME-002", skill_path.relative_to(root).as_posix(), "skill frontmatter name does not match plugin name", f"set the skill name to `{name}`"))
    if isinstance(name, str) and skill_dir.name != name:
        findings.append(Finding("MANIFEST-NAME-003", skill_dir.relative_to(root).as_posix(), "skill directory name does not match plugin name", f"rename the directory to `{name}`"))

    try:
        agent = load_yaml(agent_path)
    except ValueError as exc:
        findings.append(Finding("MANIFEST-AGENT-001", agent_path.relative_to(root).as_posix(), str(exc), "restore valid UTF-8 YAML"))
        agent = None
    if isinstance(agent, dict):
        agent_interface = agent.get("interface")
        if not isinstance(agent_interface, dict):
            findings.append(Finding("MANIFEST-AGENT-002", agent_path.relative_to(root).as_posix(), "missing `interface` mapping", "add display_name, short_description, and default_prompt"))
        else:
            for key in ("display_name", "short_description", "default_prompt"):
                if not isinstance(agent_interface.get(key), str) or not agent_interface[key].strip():
                    findings.append(Finding("MANIFEST-AGENT-003", agent_path.relative_to(root).as_posix(), f"missing non-empty `{key}`", f"add a non-empty `{key}` value"))
            default_prompt = agent_interface.get("default_prompt", "")
            if isinstance(name, str) and f"${name}" not in default_prompt:
                findings.append(Finding("MANIFEST-AGENT-004", agent_path.relative_to(root).as_posix(), "default prompt does not invoke the packaged skill", f"include `${name}` in `default_prompt`"))

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        try:
            relative.encode("ascii")
        except UnicodeEncodeError:
            findings.append(Finding("MANIFEST-ASCII-001", relative, "repository path contains non-ASCII characters", "rename the path using ASCII characters"))

    findings.extend(scan_secrets_and_absolute_paths(root))
    return findings


def run() -> int:
    parser = argparse.ArgumentParser(description="Validate Modern Flat plugin packaging and repository portability.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    return print_findings(validate(args.root))


if __name__ == "__main__":
    main_guard(run)
