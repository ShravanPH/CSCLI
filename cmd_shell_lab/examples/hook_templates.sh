  autoload -Uz add-zsh-hook
  cmd_case_open_preexec() {
    [[ -n "${CMD_CASE_OPEN_ACTIVE:-}" ]] && return
    [[ "$1" == cmd-case-open* ]] && return
    CMD_CASE_OPEN_ACTIVE=1 cmd-case-open case-open --text "$1" >/dev/tty 2>/dev/tty || true
    unset CMD_CASE_OPEN_ACTIVE
  }
  add-zsh-hook preexec cmd_case_open_preexec
