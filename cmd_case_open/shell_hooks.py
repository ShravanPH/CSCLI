from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess

HOOK_START = "# >>> cmd-case-open hooks >>>"
HOOK_END = "# <<< cmd-case-open hooks <<<"


def _read_script(script_name: str) -> str:
    script_path = Path(__file__).parent / "scripts" / script_name
    return script_path.read_text(encoding="utf-8")


def _insert_block(profile_text: str, block: str) -> str:
    start_idx = profile_text.find(HOOK_START)
    end_idx = profile_text.find(HOOK_END)

    # If hooks already exist, keep profile untouched.
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        return profile_text

    content = profile_text.rstrip()
    if content:
        return content + "\n\n" + block.strip() + "\n"
    return block.strip() + "\n"


def _write_profile(path: Path, block: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    updated = _insert_block(existing, block)
    if updated != existing:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def _reload_shell(shell: str, profile_path: Path) -> None:
    if shell == "zsh":
        if shutil.which("zsh"):
            quoted = shlex.quote(str(profile_path))
            try:
                subprocess.run(
                    ["zsh", "-ic", f"source {quoted}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            except Exception as e:
                print("Error reloading profile:", e)
        return
    raise ValueError(f"Unsupported shell: {shell}")


def _print_restart_notice(shell: str, profile_path: Path) -> None:
    print(
        "[cmd-case-open] Shell hooks installed. "
        "Restart your terminal for changes to take effect."
    )


def _detect_shell() -> str:
    if os.name == "nt":
        return "powershell"

    shell = (os.getenv("SHELL") or "").lower()
    if "pwsh" in shell or "powershell" in shell:
        return "powershell"
    return "zsh"


def _powershell_profile_path() -> Path:
    path_to_profile = ""
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", "$PROFILE"],
            capture_output=True,
        )
        path_to_profile = result.stdout.strip()
    except Exception as e:
        print("profile_error",e)
        pass
    return Path(path_to_profile.decode("utf-8"))


def _install_hooks_for_shell(shell: str) -> None:
    if shell == "zsh":
        profile_path = Path.home() / ".zshrc"
        changed = _write_profile(profile_path, _read_script("hooks.zsh"))
        if changed:
            _reload_shell(shell, profile_path)
            _print_restart_notice(shell, profile_path)
        else:
            print("cmd-case-open previously installed.")

    if shell == "powershell":
        profile_path = _powershell_profile_path()
        try:
            changed = _write_profile(profile_path, _read_script("hooks.powershell.ps1"))
            if changed:
                _print_restart_notice(shell, profile_path)
            else:
                print("cmd-case-open previously installed.")
        except Exception as e:
            print("Profile write erorr:",e)
        return
    raise ValueError(f"Unsupported shell: {shell}")


def install_hooks() -> None:
    try:
        _install_hooks_for_shell(_detect_shell())
    except Exception as e:
        print(e)
        # Never block normal CLI usage on hook installation failures.
        pass
