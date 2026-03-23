# ClawTeam Portable Skill for Codex

Portable Codex skill wrapper for `python -m clawteam`, adapted for cross-machine installation and reuse.

## What This Repository Provides

- A portable `clawteam` skill package for Codex
- A relative-path wrapper around `python -m clawteam`
- An install script for copying the skill into `~/.codex/skills/clawteam`
- A compatibility shim for older local entry points

## Install

```powershell
python scripts/install_skill.py
```

## Main Usage

```powershell
python scripts/wrapper.py run "Review the recent changes in this repo"
python scripts/wrapper.py run --strategy spawn "Fix a Python bug"
python scripts/wrapper.py run --strategy launch "Research the latest progress in quantum computing"
python scripts/wrapper.py templates
```

## Source And Attribution

This repository is a portability-focused adaptation built on top of the original ClawTeam project:

- Source project: [HKUDS/ClawTeam](https://github.com/HKUDS/ClawTeam)

The upstream package metadata for the installed `clawteam` CLI points to the same project homepage.

## Thanks

Thanks to the ClawTeam authors and maintainers for building and open-sourcing the original multi-agent coordination CLI.
