#!/usr/bin/env python
"""Portable ClawTeam wrapper for Codex skills."""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


TASK_KEYWORDS = {
    "code": [
        "代码",
        "code",
        "编程",
        "开发",
        "写程序",
        "pr",
        "review",
        "bug",
        "fix",
    ],
    "research": ["研究", "论文", "文献", "research", "paper", "分析"],
    "hedge-fund": [
        "投资",
        "基金",
        "股票",
        "金融",
        "hedge",
        "fund",
        "investment",
        "stock",
    ],
}
TEAM_BY_TYPE = {
    "code": "team-code",
    "research": "team-research",
    "hedge-fund": "team-hedge-fund",
    "general": "team-general",
}
TEMPLATE_BY_TYPE = {
    "code": "code-review",
    "research": "research-paper",
    "hedge-fund": "hedge-fund",
}
DEFAULT_COMMAND_CANDIDATES = ("codex", "qwen", "claude")
SKILL_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Route:
    task_type: str
    strategy: str
    team_name: str
    template: str | None
    command: list[str]


def detect_task_type(task: str) -> str:
    lowered = task.lower()
    for task_type, keywords in TASK_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return task_type
    return "general"


def parse_command_text(command_text: str) -> list[str]:
    if not command_text.strip():
        raise ValueError("command text cannot be empty")
    return shlex.split(command_text, posix=False)


def resolve_command_text(explicit: str | None) -> str:
    if explicit:
        return explicit

    env_value = os.environ.get("CLAWTEAM_AGENT_COMMAND")
    if env_value and env_value.strip():
        return env_value.strip()

    for candidate in DEFAULT_COMMAND_CANDIDATES:
        if shutil.which(candidate):
            return candidate

    return DEFAULT_COMMAND_CANDIDATES[0]


def resolve_data_dir(explicit: str | None) -> str | None:
    if explicit:
        return explicit

    env_value = os.environ.get("CLAWTEAM_DATA_DIR")
    if env_value and env_value.strip():
        return env_value.strip()

    return None


def base_clawteam_cmd(data_dir: str | None) -> list[str]:
    cmd = [sys.executable, "-m", "clawteam"]
    if data_dir:
        cmd.extend(["--data-dir", data_dir])
    return cmd


def build_spawn_command(args: argparse.Namespace, task_type: str, data_dir: str | None) -> Route:
    command_text = resolve_command_text(args.command)
    command = base_clawteam_cmd(data_dir)
    command.extend(["spawn", args.backend])
    command.extend(parse_command_text(command_text))
    command.extend(["--agent-name", args.agent_name, "--task", args.task])

    team_name = args.team_name or TEAM_BY_TYPE[task_type]
    command.extend(["--team", team_name])

    if args.repo:
        command.extend(["--repo", args.repo])
    if args.workspace:
        command.append("--workspace")
    if args.no_workspace:
        command.append("--no-workspace")
    if args.resume:
        command.append("--resume")

    return Route(
        task_type=task_type,
        strategy="spawn",
        team_name=team_name,
        template=None,
        command=command,
    )


def build_launch_command(args: argparse.Namespace, task_type: str, data_dir: str | None) -> Route:
    template = TEMPLATE_BY_TYPE.get(task_type)
    if not template:
        raise ValueError(f"task type '{task_type}' does not map to a built-in template")

    command = base_clawteam_cmd(data_dir)
    command.extend(["launch", template, "--goal", args.task, "--command", resolve_command_text(args.command)])

    team_name = args.team_name or TEAM_BY_TYPE[task_type]
    command.extend(["--team-name", team_name])

    if args.backend:
        command.extend(["--backend", args.backend])
    if args.repo:
        command.extend(["--repo", args.repo])
    if args.workspace:
        command.append("--workspace")
    if args.no_workspace:
        command.append("--no-workspace")

    return Route(
        task_type=task_type,
        strategy="launch",
        team_name=team_name,
        template=template,
        command=command,
    )


def build_route(args: argparse.Namespace) -> Route:
    task_type = detect_task_type(args.task)
    data_dir = resolve_data_dir(args.data_dir)

    if args.strategy == "spawn":
        return build_spawn_command(args, task_type, data_dir)
    if args.strategy == "launch":
        return build_launch_command(args, task_type, data_dir)
    if task_type in TEMPLATE_BY_TYPE:
        return build_launch_command(args, task_type, data_dir)
    return build_spawn_command(args, task_type, data_dir)


def format_shell_command(command: list[str]) -> str:
    return subprocess.list2cmdline(command)


def cmd_run(args: argparse.Namespace) -> int:
    route = build_route(args)
    print(f"skill_root: {SKILL_ROOT}")
    print(f"task_type: {route.task_type}")
    print(f"strategy: {route.strategy}")
    print(f"team_name: {route.team_name}")
    if route.template:
        print(f"template: {route.template}")
    print(f"command: {format_shell_command(route.command)}")

    if args.dry_run:
        return 0

    completed = subprocess.run(route.command, text=True)
    return completed.returncode


def cmd_templates(args: argparse.Namespace) -> int:
    command = base_clawteam_cmd(resolve_data_dir(args.data_dir))
    command.extend(["template", "list"])
    print(f"command: {format_shell_command(command)}")
    completed = subprocess.run(command, text=True)
    return completed.returncode


def cmd_raw(args: argparse.Namespace) -> int:
    command = base_clawteam_cmd(resolve_data_dir(args.data_dir))
    command.extend(args.raw_args)
    print(f"command: {format_shell_command(command)}")
    if args.dry_run:
        return 0
    completed = subprocess.run(command, text=True)
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Portable ClawTeam wrapper for Codex skills")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    run_parser = subparsers.add_parser("run", help="Route a natural-language task into ClawTeam")
    run_parser.add_argument("task", help="Natural-language task to route")
    run_parser.add_argument(
        "--strategy",
        choices=["auto", "spawn", "launch"],
        default="auto",
        help="Routing strategy",
    )
    run_parser.add_argument("--team-name", help="Override team name")
    run_parser.add_argument("--agent-name", default="agent", help="Agent name for spawn")
    run_parser.add_argument("--backend", default="subprocess", help="ClawTeam backend")
    run_parser.add_argument(
        "--command",
        help="Agent command. Defaults to CLAWTEAM_AGENT_COMMAND or auto-detected codex/qwen/claude",
    )
    run_parser.add_argument("--repo", help="Repo path for the task")
    run_parser.add_argument("--data-dir", help="Override ClawTeam data directory")
    run_parser.add_argument("--workspace", action="store_true", help="Enable isolated workspace")
    run_parser.add_argument("--no-workspace", action="store_true", help="Disable workspace")
    run_parser.add_argument("--resume", action="store_true", help="Resume a previous spawn session")
    run_parser.add_argument("--dry-run", action="store_true", help="Print the resolved command only")
    run_parser.set_defaults(func=cmd_run)

    templates_parser = subparsers.add_parser("templates", help="List built-in and user templates")
    templates_parser.add_argument("--data-dir", help="Override ClawTeam data directory")
    templates_parser.set_defaults(func=cmd_templates)

    raw_parser = subparsers.add_parser("raw", help="Pass through a raw ClawTeam command")
    raw_parser.add_argument("raw_args", nargs=argparse.REMAINDER, help="Arguments after `python -m clawteam`")
    raw_parser.add_argument("--data-dir", help="Override ClawTeam data directory")
    raw_parser.add_argument("--dry-run", action="store_true", help="Print the resolved command only")
    raw_parser.set_defaults(func=cmd_raw)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        parser.error(str(exc))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
