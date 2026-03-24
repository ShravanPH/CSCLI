# cmd_shell_lab

Minimal Python boilerplate for fast CLI iteration.

This repo intentionally does **not** implement any product feature logic.
It only provides examples for:
- reading terminal input
- deriving deterministic seeds from input text
- splitting shell command text safely
- running a long-lived per-shell background worker
- wiring shell hooks to emit command events to that worker

## Quick start

```bash
cd cmd_shell_lab
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cmd-shell-lab --help
```

## Example commands

```bash
cmd-shell-lab input-demo --text "git status"
echo "ls -la" | cmd-shell-lab input-demo
cmd-shell-lab seed-demo --text "npm test"
cmd-shell-lab seed-demo --text "npm test" --no-anim
cmd-shell-lab split-demo --text "python app.py --mode quick"
cmd-shell-lab worker-ensure --session-id "demo-shell"
cmd-shell-lab emit --session-id "demo-shell" --text "git status"
cmd-shell-lab worker-status --session-id "demo-shell"
cmd-shell-lab worker-stop --session-id "demo-shell"
cmd-shell-lab scaffold-feature --name terminal-animation
```

## Shell hook examples (templates)

These snippets are templates only.

### zsh startup + `preexec`

```zsh
# ~/.zshrc
export CMD_SHELL_LAB_SESSION="${HOST}-${$}"
cmd-shell-lab worker-ensure --session-id "$CMD_SHELL_LAB_SESSION" >/dev/null 2>&1

cmd_shell_lab_preexec() {
  cmd-shell-lab emit --session-id "$CMD_SHELL_LAB_SESSION" --text "$1" >/dev/null 2>&1
}

cmd_shell_lab_shutdown() {
  cmd-shell-lab worker-stop --session-id "$CMD_SHELL_LAB_SESSION" >/dev/null 2>&1
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec cmd_shell_lab_preexec
add-zsh-hook zshexit cmd_shell_lab_shutdown
```

### bash startup + `DEBUG` trap

```bash
# ~/.bashrc
export CMD_SHELL_LAB_SESSION="${HOSTNAME:-bash}-${$}"
cmd-shell-lab worker-ensure --session-id "$CMD_SHELL_LAB_SESSION" >/dev/null 2>&1

cmd_shell_lab_debug_hook() {
  cmd-shell-lab emit --session-id "$CMD_SHELL_LAB_SESSION" --text "$BASH_COMMAND" >/dev/null 2>&1
}
trap 'cmd_shell_lab_debug_hook' DEBUG

cmd_shell_lab_shutdown() {
  cmd-shell-lab worker-stop --session-id "$CMD_SHELL_LAB_SESSION" >/dev/null 2>&1
}
trap 'cmd_shell_lab_shutdown' EXIT
```

## Project layout

```text
cmd_shell_lab/
  pyproject.toml
  README.md
  cmd_shell_lab/
    __init__.py
    cli.py
    examples.py
```

## Notes

- Keep command handlers tiny so iteration remains fast.
- Worker logs are written to `~/.local/state/cmd_shell_lab/` when writable, otherwise `/tmp/cmd_shell_lab_state/`.
- Add new subcommands before implementing feature behavior.
- Prefer deterministic test helpers while exploring ideas.
