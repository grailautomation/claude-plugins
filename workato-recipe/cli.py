#!/usr/bin/env python3
"""Stable CLI entry point for Workato recipe extraction and fidelity utilities."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent

COMMANDS = {
    "extract": PLUGIN_ROOT / "skills" / "workato-recipe" / "scripts" / "extract_views.py",
    "check-fidelity": PLUGIN_ROOT / "scripts" / "check_fidelity.py",
    "check-compat": PLUGIN_ROOT / "scripts" / "check_compat.py",
}
SELF_TEST = PLUGIN_ROOT / "scripts" / "run_self_test.sh"


def usage() -> int:
    print(
        "Usage: cli.py {extract|check-fidelity|check-compat|self-test} [ARGS...]\n\n"
        "Stable external interface for the workato-recipe plugin."
    )
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        return usage()

    command = argv[1]
    if command == "self-test":
        completed = subprocess.run(["bash", str(SELF_TEST), *argv[2:]], cwd=PLUGIN_ROOT)
        return completed.returncode

    script = COMMANDS.get(command)
    if script is None:
        print(f"ERROR: Unknown command: {command}", file=sys.stderr)
        return 2

    completed = subprocess.run([sys.executable, str(script), *argv[2:]], cwd=Path.cwd())
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
