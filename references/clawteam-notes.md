# ClawTeam Notes

## Task Type Mapping

- `code`: `code`, `pr`, `review`, `bug`, `fix`, plus the Chinese keywords kept in `scripts/wrapper.py`
- `research`: `research`, `paper`, plus the Chinese keywords kept in `scripts/wrapper.py`
- `hedge-fund`: `hedge`, `fund`, `investment`, `stock`, plus the Chinese keywords kept in `scripts/wrapper.py`
- `general`: anything else

## Strategy Mapping

- `auto`
- `code` -> `launch code-review`
- `research` -> `launch research-paper`
- `hedge-fund` -> `launch hedge-fund`
- `general` -> `spawn subprocess <agent-command>`
- `spawn`
- always use `spawn`
- `launch`
- require a known template mapping; fail for `general`

## Default Agent Command

- First use `CLAWTEAM_AGENT_COMMAND` if it is set.
- Otherwise probe for `codex`, then `qwen`, then `claude`.
- Fallback is `codex`.

## Data Directory

- Pass `--data-dir` when the user explicitly wants a non-default ClawTeam state directory.
- Otherwise let `python -m clawteam` use its own default `~/.clawteam`.

## Portability Rule

This skill is intended to live in any copied folder first, then be installed into `~/.codex/skills/clawteam` with `python scripts/install_skill.py`.
