# cmd_case_open

A CLI project that simulates **Counter-Strike–style case openings** directly in your terminal.

Open cases, reveal randomized items with rarity tiers, and track your inventory all from your shell.

## Demo

 ![Demo GIF](cmd_case_open/assets/demo.gif)

---

##  Features

-  Counter-Strike–inspired case opening system
-  Rarity-based item generation
-  Persistent inventory + stats tracking
-  Shell-integrated commands (run after any terminal command)
-  Supports Zsh and PowerShell

---

## Installation

You can install `cmd_case_open` in two ways:

---

### Option 1: Install via pip (Recommended)

```bash
pip install cmd-case-open
````

Then initialize the CLI:

```bash
cmd-case-open
```

During setup:

* Your shell configuration (`.zshrc` or PowerShell profile) will be automatically updated
* You will be prompted to **restart your terminal**

After restarting, the CLI is fully active.

---

### Option 2: Install from source (Git clone)

Clone the repository:

```bash
git clone https://github.com/ShravanPH/CSCLI.git
cd CSCLI
```

Install locally in editable mode:

```bash
pip install -e .
```

Run setup:

```bash
cmd-case-open
```

Restart your terminal when prompted.


## How It Works

After installation and terminal restart:

Every time you run a command in your terminal, you’ll be given the option to:

```bash
case-reveal        # Open a case
case-reveal-stats  # View your inventory + stats
```

This behavior is powered by **shell hooks** that are automatically added to:

* `~/.zshrc` (Zsh)
* PowerShell profile (Windows)


## Shell Integration

The CLI modifies your shell configuration to inject its behavior.

* The startup + execution logic lives inside your shell config files
* This controls when `cmd-case-open` is triggered

### Customization

If you want to tweak behavior (frequency, triggers, etc.), you can edit:

* `~/.zshrc`
* PowerShell profile


## Project Structure

```
CSCLI/
```

Contains the core logic for:

* Case randomization
* Item rarity system
* Rendering output
* Case data definitions


##  Data Storage

Inventory data is stored locally as JSON Lines:

Primary location:

```
~/.local/state/cmd_case_open/inventory.jsonl
```

Fallback:

```
/tmp/cmd_case_open_state/inventory.jsonl
```

Each entry includes:

* Timestamp
* Item name
* Rarity
* Rarity key
* Colorized rarity snapshot


##  Commands

### Setup

```bash
cmd-case-open
```

### Runtime Commands

```bash
case-reveal
case-reveal-stats
```


##  Supported Shells

* Zsh
* PowerShell


##  Notes

* First run modifies your shell config automatically
* A terminal restart is required after installation
* Behavior is shell-driven — not a continuously running process


##  Future Improvements (Ideas)

* More cases and skins
* Inventory UI improvements
* Drop rate customization



##  License

* MIT License


##  Contributing

Contributions, issues, and ideas are welcome!

