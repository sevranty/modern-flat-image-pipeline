from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

VALID_SCENE = Path("tests/validation/scene/valid.yaml")
INVALID_SCENES = {
    Path("tests/validation/scene/invalid-style.yaml"): "SCENE-STYLE-001",
    Path("tests/validation/scene/invalid-safe-area.yaml"): "SCENE-SAFE-001",
    Path("tests/validation/scene/invalid-conflict.yaml"): "SCENE-CONFLICT-001",
}
VALID_PROMPT = Path("tests/validation/prompt/valid.txt")
INVALID_PROMPTS = {
    Path("tests/validation/prompt/invalid-photorealistic.txt"): "PROMPT-DRIFT-001",
    Path("tests/validation/prompt/invalid-brand.txt"): "PROMPT-BRAND-001",
    Path("tests/validation/prompt/invalid-light.txt"): "PROMPT-LIGHT-001",
    Path("tests/validation/prompt/invalid-artist.txt"): "PROMPT-ARTIST-001",
}


def run_command(root: Path, args: list[str], expect_success: bool, expected_rule: str | None = None) -> tuple[bool, str]:
    completed = subprocess.run(
        [sys.executable, *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    success = completed.returncode == 0
    if expect_success and not success:
        return False, f"command failed unexpectedly: {' '.join(args)}\n{output}"
    if not expect_success and success:
        return False, f"negative fixture passed unexpectedly: {' '.join(args)}\n{output}"
    if expected_rule and expected_rule not in output:
        return False, f"negative fixture did not emit {expected_rule}: {' '.join(args)}\n{output}"
    return True, output


def run() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic repository and fixture validation.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    checks: list[tuple[str, bool, str]] = []

    checks.append(("manifest", *run_command(root, ["scripts/validate_manifest.py", "."], True)))
    checks.append(("evaluation", *run_command(root, ["scripts/validate_evaluation.py", "."], True)))
    checks.append(("scene-valid", *run_command(root, ["scripts/validate_scene_spec.py", str(VALID_SCENE)], True)))
    checks.append(("prompt-valid", *run_command(root, ["scripts/validate_prompt.py", str(VALID_PROMPT)], True)))

    for path, rule in INVALID_SCENES.items():
        checks.append((f"scene-negative:{path.name}", *run_command(root, ["scripts/validate_scene_spec.py", str(path)], False, rule)))
    for path, rule in INVALID_PROMPTS.items():
        checks.append((f"prompt-negative:{path.name}", *run_command(root, ["scripts/validate_prompt.py", str(path)], False, rule)))

    failures = 0
    for name, ok, output in checks:
        state = "PASS" if ok else "FAIL"
        print(f"{state} {name}")
        if not ok:
            failures += 1
            print(output.rstrip())
    print(f"SUMMARY checks={len(checks)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run())
