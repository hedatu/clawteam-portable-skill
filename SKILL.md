---
name: clawteam
description: Use this skill when the user explicitly asks to use ClawTeam, wants a local multi-agent handoff, wants to route natural-language work into `python -m clawteam`, or wants a portable ClawTeam wrapper that can be installed on another Codex machine.
---

# ClawTeam

Use this skill as a thin wrapper around `python -m clawteam`.

## Install Or Update The Skill

From the skill source directory, run:

```powershell
python scripts/install_skill.py
```

That copies this folder into the active Codex skills directory as `clawteam`.

## Primary Entry Point

Use the wrapper:

```powershell
python scripts/wrapper.py run "Review the recent changes in this repo"
python scripts/wrapper.py run --strategy spawn "Fix a Python bug"
python scripts/wrapper.py run --strategy launch "Research the latest progress in quantum computing"
python scripts/wrapper.py templates
python scripts/wrapper.py raw team discover
```

## Routing Rules

- Prefer `run` for normal natural-language dispatch.
- Default strategy is `auto`.
- In `auto`, code and review tasks map to the `code-review` template.
- In `auto`, research and paper tasks map to the `research-paper` template.
- In `auto`, investment, stock, and fund tasks map to the `hedge-fund` template.
- In `auto`, anything else falls back to a single-agent `spawn` flow under `team-general`.
- Use `--strategy spawn` when the user wants one agent only.
- Use `--strategy launch` when the user explicitly wants the template team path.

## Portability Rules

- Keep all paths relative to this skill directory.
- Do not hardcode `C:\Users\...\.codex\skills\...` into wrappers.
- Use `CLAWTEAM_DATA_DIR` when the user wants a custom ClawTeam state directory.
- Use `CLAWTEAM_AGENT_COMMAND` when the machine should default to a specific agent command.
- Read `references/clawteam-notes.md` if you need the command-shape details.
