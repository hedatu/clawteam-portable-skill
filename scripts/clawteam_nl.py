#!/usr/bin/env python
"""Compatibility shim that runs the portable ClawTeam wrapper."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


WRAPPER_PATH = Path(__file__).resolve().with_name("wrapper.py")


def main() -> int:
    if not WRAPPER_PATH.exists():
        print(f"wrapper not found: {WRAPPER_PATH}", file=sys.stderr)
        return 1

    if len(sys.argv) > 1:
        command = [sys.executable, str(WRAPPER_PATH), "run", " ".join(sys.argv[1:])]
        return subprocess.run(command).returncode

    print("Enter a task. Press Ctrl+C to exit.")
    try:
        while True:
            task = input("> ").strip()
            if not task:
                continue
            if task.lower() in {"quit", "exit"}:
                return 0
            command = [sys.executable, str(WRAPPER_PATH), "run", task]
            result = subprocess.run(command)
            if result.returncode != 0:
                return result.returncode
    except KeyboardInterrupt:
        print()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
