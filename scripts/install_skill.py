#!/usr/bin/env python
"""Install the portable ClawTeam skill into the local Codex skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CODEX_HOME = Path.home() / ".codex"


def codex_home_from_env() -> Path:
    env_value = os.environ.get("CODEX_HOME")
    if env_value and env_value.strip():
        return Path(env_value).expanduser()
    return DEFAULT_CODEX_HOME


def ignore_filter(_dir: str, names: list[str]) -> set[str]:
    ignored = {"__pycache__", ".git", ".DS_Store"}
    return {name for name in names if name in ignored or name.endswith(".pyc")}


def install(target_dir: Path, force: bool) -> Path:
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    if target_dir.exists():
        if not force:
            raise FileExistsError(f"target already exists: {target_dir}")
        shutil.rmtree(target_dir)

    shutil.copytree(SKILL_ROOT, target_dir, ignore=ignore_filter)
    return target_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the portable ClawTeam skill for Codex")
    parser.add_argument(
        "--codex-home",
        help="Override CODEX_HOME. Defaults to CODEX_HOME or ~/.codex",
    )
    parser.add_argument(
        "--skill-name",
        default="clawteam",
        help="Installed skill directory name",
    )
    parser.add_argument(
        "--no-force",
        action="store_true",
        help="Do not overwrite an existing installed skill",
    )
    args = parser.parse_args()

    codex_home = Path(args.codex_home).expanduser() if args.codex_home else codex_home_from_env()
    target_dir = codex_home / "skills" / args.skill_name
    installed_dir = install(target_dir, force=not args.no_force)

    print(f"source: {SKILL_ROOT}")
    print(f"installed: {installed_dir}")
    print(f"wrapper: {installed_dir / 'scripts' / 'wrapper.py'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
