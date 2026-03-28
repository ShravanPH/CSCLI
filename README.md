# cmd_case_open

CLI for terminal case-opening experiments.

## Quick start

```bash
cd cmd_case_open
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cmd-case-open --help
```

## Commands

```bash
cmd-case-open case-open --text "git status"
cmd-case-open case-open --text "npm test" --no-anim
cmd-case-open inventory-stats
cmd-case-open install-shell-hooks --shell auto
```

## Storage

Inventory entries are appended to:

- `~/.local/state/cmd_case_open/inventory.jsonl`
- fallback: `/tmp/cmd_case_open_state/inventory.jsonl`

Each entry stores timestamp, name, rarity, rarity key, and a colorized rarity snapshot.

Shell hooks are auto-installed on first CLI run when possible.
Set `CMD_CASE_OPEN_AUTO_HOOKS=0` to opt out.

## Package layout

```text
cmd_case_open/
  __init__.py
  CSCLI/
    __main__.py
    CSCLI.py
    parser.py
    handlers.py
  core/
    constants.py
    utils.py
    rendering.py
  domain/
    case_catalog.py
  scripts/
    hooks.zsh
    hooks.powershell.ps1
  inventory.py
  data/
    spectrum-case.json
```
