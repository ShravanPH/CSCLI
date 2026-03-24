  autoload -Uz add-zsh-hook
  cmd_shell_lab_preexec() {
    [[ -n "${CMD_SHELL_LAB_ACTIVE:-}" ]] && return
    [[ "$1" == cmd-shell-lab* ]] && return
    CMD_SHELL_LAB_ACTIVE=1 cmd-shell-lab input-demo --text "$1" >/dev/tty 2>/dev/tty || true
    unset CMD_SHELL_LAB_ACTIVE
  }
  add-zsh-hook preexec cmd_shell_lab_preexec