<div align="center">

# RUN-GIT

**Git Operations Made Effortless** — One command to add, commit, pull, and push with smart auto-messages.

[![PyPI version](https://badge.fury.io/py/run-git.svg)](https://badge.fury.io/py/run-git)
[![Downloads](https://static.pepy.tech/badge/run-git)](https://pepy.tech/project/run-git)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/himanshu231204/gitpush)](https://github.com/himanshu231204/gitpush/stargazers)

</div>

---

## Overview

RUN-GIT is a Python-powered CLI that simplifies Git workflows into single, intuitive commands. It handles the common add-commit-pull-push sequence automatically, generates meaningful commit messages, provides interactive branch management, and integrates with GitHub for repository creation.

**Use case**: Developers who run the same Git commands dozens of times daily and want a faster way to commit and push.

[📦 Installation](#installation) · [🚀 Quick Start](#quick-start) · [📖 Commands](#command-reference) · [🏗️ Architecture](#architecture)

---

## Features

| Feature | Description |
|---------|-------------|
| **One-Command Push** | `run-git push` executes add → commit → pull → push automatically |
| **Smart Commit Messages** | Auto-generates Conventional Commits style messages based on staged changes |
| **Interactive TUI** | Full terminal menu for navigation without memorizing flags |
| **GitHub Integration** | Create public/private repositories directly from CLI |
| **Branch Management** | Create, switch, merge, and delete branches with simple commands |
| **Commit Graph** | Visualize commit history with ASCII graphs and file diffs |
| **Secret File Guard** | Warns before accidentally pushing sensitive files (`.env`, tokens) |
| **Conflict Helper** | Guided interactive merge conflict resolution |
| **Rich Status View** | Color-coded table-based status output |

---

## Installation

```bash
pip install run-git
```

Requires **Python 3.8+**. Works on macOS, Linux, and Windows.

> **First time**: Set your GitHub token with `run-git init`
> **Upgrade**: `pip install --upgrade run-git`

---

## Quick Start

### Push changes
```bash
run-git push                        # auto commit message + push
run-git push -m "feat: add login"  # custom commit message
```

### Interactive menu
```bash
run-git          # full TUI — no commands to memorize
```

### Create GitHub repository
```bash
run-git new my-project                              # guided wizard
run-git new my-project --quick                      # defaults, no prompts
run-git new my-api -d "REST API" --public -g Python -l MIT  # full options
```

---

## Command Reference

| Command | Description |
|---------|-------------|
| `run-git` | Open the interactive TUI menu |
| `run-git push` | Add, commit, pull, and push in one step |
| `run-git push -m "<msg>"` | Push with custom commit message |
| `run-git new <name>` | Create a new GitHub repository |
| `run-git init` | Initialize a local or cloned repository |
| `run-git status` | Rich color-coded repository status |
| `run-git log` | Formatted commit history |
| `run-git graph` | Visual commit history (table view) |
| `run-git graph --graph` | ASCII graph with branch lines |
| `run-git branch` | List all branches |
| `run-git branch <name>` | Create a new branch |
| `run-git switch <name>` | Switch to a branch |
| `run-git merge <name>` | Merge a branch into current |
| `run-git pull` | Pull latest changes |
| `run-git sync` | Pull then push (keep in sync) |
| `run-git remote` | Show configured remotes |
| `run-git stash` | Stash uncommitted changes |
| `run-git undo` | Undo last commit (keeps changes staged) |
| `run-git config` | Manage configuration |
| `run-git --version` | Show installed version |
| `run-git --help` | Show help for any command |

---

## Architecture

```
gitpush/
├── cli.py                 # Main CLI entry point (Click)
├── commands/              # Modular command handlers
│   ├── push.py           # Push command
│   ├── init.py           # Init command
│   ├── status.py         # Status & log commands
│   ├── branch.py         # Branch operations
│   ├── github.py         # GitHub integration
│   └── graph.py          # Commit graph visualization
├── core/                 # Business logic
│   ├── git_operations.py # Git operations
│   ├── commit_generator.py # Auto commit messages
│   └── conflict_resolver.py # Merge conflict handling
├── ui/                   # Terminal UI (Rich, questionary)
├── utils/                # Utilities (validators, formatters)
├── config/               # Configuration management
└── exceptions.py        # Custom exceptions
```

**Design principles**:
- **Separation of concerns**: `commands/` (thin orchestration), `core/` (business logic), `ui/` (terminal rendering)
- **Testable**: Core logic independent of CLI dependencies
- **Extensible**: New commands added as isolated modules

---

## Auto Commit Messages

RUN-GIT analyzes staged changes and generates [Conventional Commits](https://www.conventionalcommits.org/) style messages:

```
feat: add authentication module (3 files added)
fix: update user validation logic (2 files modified)
docs: update README (1 file modified)
refactor: remove deprecated helper functions (2 files deleted)
```

---

## Comparison

| | Raw Git | GitHub CLI (`gh`) | RUN-GIT |
|---|---|---|---|
| Push in one command | ❌ | ❌ | ✅ |
| Auto commit messages | ❌ | ❌ | ✅ |
| Interactive TUI | ❌ | Partial | ✅ |
| Create GitHub repos | ❌ | ✅ | ✅ |
| Secret file warnings | ❌ | ❌ | ✅ |

> RUN-GIT is a speed layer on top of Git — not a replacement. Use it for daily work; reach for `git` or `gh` when you need fine-grained control.

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

```bash
# Clone and setup
git clone https://github.com/himanshu231204/gitpush.git
cd gitpush

# Install in development mode
pip install -e ".[test]"

# Run tests
pytest
```

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Author

**Himanshu Kumar** — [@himanshu231204](https://github.com/himanshu231204)

---

<div align="center">

If RUN-GIT saves you time, please consider giving it a ⭐ — it helps others find the project!

[![Star History Chart](https://api.star-history.com/svg?repos=himanshu231204/gitpush&type=Date)](https://star-history.com/#himanshu231204/gitpush&Date)

</div>