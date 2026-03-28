# Roadmap (From Current State)

## V1.0 - Packaging + Multi-shell Bootstrap

### Goals
- Ship a clean CLI package (`cmd-case-open`) ready for public install.
- Support both zsh and PowerShell shell-hook workflows.
- Auto-install shell hooks on first CLI invocation after install.
- Keep install experience simple for `pipx` users.

### Scope
- In scope:
  - Shell-hook installer command (`install-shell-hooks`)
  - zsh hook block template + PowerShell profile draft block
  - Shell auto-detection (`zsh|powershell|auto`)
  - Profile file patching with marker-based replace/update
  - Best-effort profile reload command execution
  - Auto-hook installation trigger in CLI startup
  - CLI refactor entry module to `CSCLI`
- Out of scope for V1:
  - Smoke tests (explicitly deferred)
  - Full Windows terminal matrix QA

### Milestones
1. CLI structure and command surface
- Add `install-shell-hooks` subcommand.
- Add options: `--shell`, `--no-reload`, `--force`.

2. Hook installer engine
- Add shared shell-hook module with:
  - marker-based block upsert
  - zsh profile path handling
  - PowerShell profile path detection
  - optional profile reload helpers

3. Hook templates
- zsh: mirror existing behavior (`pending` command, teaser, `case-reveal`, stats).
- PowerShell: draft equivalent using `prompt` + history tracking + reveal functions.

4. Auto-install strategy for pipx flow
- On CLI startup, if hooks are missing and shell is detectable, attempt one-time install.
- Respect env-based opt-out (future): `CMD_CASE_OPEN_AUTO_HOOKS=0`.

5. Documentation
- Update README with:
  - pipx install path
  - hook install command
  - shell-specific notes
  - profile reload caveat (subprocess vs parent shell session)

### Risks and mitigations
- Profile write permissions may fail.
  - Mitigation: explicit error messaging + fallback manual instructions.
- Shell reload from child process doesn’t mutate parent shell session.
  - Mitigation: run best-effort reload and still print exact manual command.
- PowerShell host differences (Windows PowerShell vs pwsh).
  - Mitigation: detect profile path via `pwsh` when available, else default profile path.

### Acceptance criteria
- `cmd-case-open --help` includes `install-shell-hooks`.
- `cmd-case-open install-shell-hooks --shell zsh` writes marker-managed block to `~/.zshrc`.
- `cmd-case-open install-shell-hooks --shell powershell` writes marker-managed block to PowerShell profile.
- First CLI run can auto-install hooks when possible.
- Existing `case-reveal` and `case-reveal stats` behavior remains functional.
