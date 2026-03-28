# TODO: Verify entire shell logic with zsh
# >>> cmd-case-open hooks >>>
if (-not $global:CMD_CASE_OPEN_HOOKS_READY) {
  $global:CMD_CASE_OPEN_HOOKS_READY = $true
  $global:CMD_CASE_OPEN_PENDING_CMD = ""
  $global:CMD_CASE_OPEN_LAST_HISTORY_ID = 0
  $global:CMD_CASE_OPEN_ACTIVE = $false

  if (-not $global:CMD_CASE_OPEN_ORIGINAL_PROMPT) {
    $existingPrompt = Get-Command prompt -CommandType Function -ErrorAction SilentlyContinue
    if ($existingPrompt) {
      $global:CMD_CASE_OPEN_ORIGINAL_PROMPT = $existingPrompt.ScriptBlock
    } else {
      $global:CMD_CASE_OPEN_ORIGINAL_PROMPT = { "PS " + (Get-Location) + "> " }
    }
  }

  function global:Invoke-CmdCaseOpenTease {
    try {
      $teaseLine = "[=={*}==>] Run: case-reveal | PS: case-reveal stats"
      $tte = Get-Command tte -ErrorAction SilentlyContinue
      if ($tte) {
        $teaseLine | tte --frame-rate 30 --canvas-width 0 --existing-color-handling ignore colorshift --gradient-steps 4 --gradient-frames 1 --cycles 1 --no-loop | Out-Host
      } else {
        Write-Host $teaseLine
      }
    } catch {
      Write-Host "[=={*}==>] Run: case-reveal | PS: case-reveal stats"
    }
  }

  function global:case-reveal {
    param([string]$Action)
    if ($Action -eq "stats") {
      cmd-case-open inventory-stats
      return
    }

    if ([string]::IsNullOrWhiteSpace($global:CMD_CASE_OPEN_PENDING_CMD)) {
      Write-Host "No pending drop."
      return
    }

    $cmdText = $global:CMD_CASE_OPEN_PENDING_CMD
    $global:CMD_CASE_OPEN_PENDING_CMD = ""
    $global:CMD_CASE_OPEN_ACTIVE = $true
    try {
      cmd-case-open case-open --no-anim --text $cmdText
    } finally {
      $global:CMD_CASE_OPEN_ACTIVE = $false
    }
  }

  function global:case-reveal-stats {
    case-reveal stats
  }

  function global:prompt {
    if (-not $global:CMD_CASE_OPEN_ACTIVE) {
      try {
        $last = Get-History -Count 1 -ErrorAction SilentlyContinue
        if ($last -and $last.Id -gt $global:CMD_CASE_OPEN_LAST_HISTORY_ID) {
          $global:CMD_CASE_OPEN_LAST_HISTORY_ID = $last.Id
          $line = $last.CommandLine.Trim()
          $skip =
            [string]::IsNullOrWhiteSpace($line) -or
            $line -match 'cmd-case-open' -or
            $line -match 'case-open' -or
            $line -match 'case-reveal' -or
            $line -match '^clear($|\\s)' -or
            $line -match '^cls($|\\s)'

          if (-not $skip) {
            $global:CMD_CASE_OPEN_PENDING_CMD = $line
            Invoke-CmdCaseOpenTease
          }
        }
      } catch {}
    }

    & $global:CMD_CASE_OPEN_ORIGINAL_PROMPT
  }
}
# <<< cmd-case-open hooks <<<
