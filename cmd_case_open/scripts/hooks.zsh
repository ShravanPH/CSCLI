# >>> cmd-case-open hooks >>>
if [[ -o interactive && -z "${CMD_CASE_OPEN_HOOKS_READY:-}" ]]; then
  autoload -Uz add-zsh-hook
  typeset -g CMD_CASE_OPEN_PENDING_CMD=""
  typeset -g CMD_CASE_OPEN_LAST_SEEN_HISTNO="${HISTCMD:-0}"

  cmd_case_open_should_skip_command() {
    local cmd="$1"
    [[ -z "$cmd" ]] && return 0
    [[ "$cmd" == *cmd-case-open* ]] && return 0
    [[ "$cmd" == *case-open* ]] && return 0
    [[ "$cmd" == *case-reveal* ]] && return 0
    [[ "$cmd" == "clear" ]] && return 0
    [[ "$cmd" == "clear "* ]] && return 0
    [[ "$cmd" == source\ ~/.zshrc* ]] && return 0
    [[ "$cmd" == .\ ~/.zshrc* ]] && return 0
    return 1
  }

  cmd_case_open_postexec() {
    [[ -n "${CMD_CASE_OPEN_ACTIVE:-}" ]] && return
    [[ -t 1 ]] || return
    local current_histno="${HISTCMD:-0}"
    [[ "$current_histno" -le "${CMD_CASE_OPEN_LAST_SEEN_HISTNO:-0}" ]] && return
    CMD_CASE_OPEN_LAST_SEEN_HISTNO="$current_histno"
    local typed_command
    typed_command="$(fc -ln -1 2>/dev/null)"
    typed_command="${typed_command#"${typed_command%%[![:space:]]*}"}"
    cmd_case_open_should_skip_command "$typed_command" && return
    CMD_CASE_OPEN_PENDING_CMD="$typed_command"

    local tease_messages=(
      "A rare terminal drop is waiting:"
      "Loot signal detected:"
      "Your next pull is queued:"
      "Hidden reward armed:"
    )
    local case_reveal_message="case-reveal"
    local stats_message="case-reveal-stats"
    local tease_art_start="[=={*}==>]"
    local tease_art_end="[<=={*}==]"
    local choice=$(( (RANDOM % ${#tease_messages[@]}) + 1 ))
    local tease_line="${tease_messages[$choice]}"
    local tease_block="${tease_line} ""${case_reveal_message}"$' | '"${stats_message}"

    # Keep teaser quick and non-blocking so the prompt returns immediately.
    if command -v tte >/dev/null 2>&1; then
      print -r -- "$tease_block" | tte --frame-rate 30 --canvas-width 0 --existing-color-handling ignore colorshift --gradient-steps 4 --gradient-frames 1 --cycles 1 --no-loop --travel-direction radial    --final-gradient-stops "#808080" --final-gradient-steps 1 >/dev/tty 2>/dev/tty || print -r -- "$tease_block" >/dev/tty 
    else
      print -r -- "$tease_block" >/dev/tty
    fi
  }

  cmd_case_open_reveal() {
    [[ -z "${CMD_CASE_OPEN_PENDING_CMD:-}" ]] && { print -r -- "No pending drop."; return 0; }
    local typed_command="$CMD_CASE_OPEN_PENDING_CMD"
    CMD_CASE_OPEN_PENDING_CMD=""
    CMD_CASE_OPEN_ACTIVE=1 cmd-case-open case-open --text "$typed_command" >/dev/tty 2>/dev/tty || true
    unset CMD_CASE_OPEN_ACTIVE
  }

  add-zsh-hook precmd cmd_case_open_postexec
  alias case-reveal='cmd_case_open_reveal'
  alias case-reveal-stats='cmd-case-open inventory-stats'
  typeset -g CMD_CASE_OPEN_HOOKS_READY=1
fi
# <<< cmd-case-open hooks <<<
