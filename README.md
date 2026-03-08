# RUN-GIT - Git Made Easy 🚀

```
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃                                                                    ┃
┃    ██████╗ ██╗   ██╗███╗   ██╗      ██████╗ ██╗████████╗         ┃
┃    ██╔══██╗██║   ██║████╗  ██║     ██╔════╝ ██║╚══██╔══╝         ┃
┃    ██████╔╝██║   ██║██╔██╗ ██║     ██║  ███╗██║   ██║            ┃
┃    ██╔══██╗██║   ██║██║╚██╗██║     ██║   ██║██║   ██║            ┃
┃    ██║  ██║╚██████╔╝██║ ╚████║     ╚██████╔╝██║   ██║            ┃
┃    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═════╝ ╚═╝   ╚═╝            ┃
┃                                                                    ┃
┃   ═══════════════════════════════════════════════════════════     ┃
┃                                                                    ┃
┃   ⚡ Git Operations Made Effortless                               ┃
┃   🎯 One Command | Zero Hassle | Full Control                     ┃
┃                                                                    ┃
┃   ┌──────────────────────────────────────────────────────────┐   ┃
┃   │  Developer    : Himanshu Kumar                           │   ┃
┃   │  GitHub       : @himanshu231204                          │   ┃
┃   │  Repository   : github.com/himanshu231204/gitpush        │   ┃
┃   │  Version      : v1.0.0                                   │   ┃
┃   │  License      : MIT                                      │   ┃
┃   └──────────────────────────────────────────────────────────┘   ┃
┃                                                                    ┃
┃   Type 'run-git help' to get started                              ┃
┃                                                                    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
```
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/run-git?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/run-git)
[![PyPI version](https://badge.fury.io/py/run-git.svg)](https://badge.fury.io/py/run-git)
[![Tests](https://github.com/himanshu231204/gitpush/workflows/Tests/badge.svg)](https://github.com/himanshu231204/gitpush/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**One Command To Rule Them All**

RUN-GIT is the ultimate Git automation tool designed to make Git operations effortless for developers of all skill levels. Say goodbye to complex Git commands and hello to simplicity!

Created by **Himanshu Kumar** ([@himanshu231204](https://github.com/himanshu231204))

---

## 🎯 Features

- ⚡ **Quick Push**: One command to add, commit, pull, and push
- 🤖 **Auto Commit Messages**: Intelligent commit message generation
- 🔀 **Interactive Conflict Resolution**: Easy-to-use conflict handling
- 🌿 **Branch Management**: Create, switch, delete, and merge branches effortlessly
- 📊 **Beautiful Status Display**: Rich terminal UI with colors and tables
- 🔐 **Sensitive File Detection**: Warns about .env, secrets, and credentials
- 🎨 **Interactive Mode**: Full TUI menu for all operations

---

## 📦 Installation

```bash
pip install run-git
```

---

## 🚀 Quick Start

### 1. Initialize Repository
```bash
# New repository
run-git init

# Clone existing repository
run-git init https://github.com/user/repo.git
```

### 2. Quick Push (Most Common Use Case)
```bash
# Add, commit, pull, and push in one command!
run-git push

# With custom commit message
run-git push -m "Add new feature"
```

### 3. Interactive Mode
```bash
# Just type run-git for interactive menu
run-git
```

---

## 📖 Usage

### Basic Commands

```bash
# Push changes
run-git push

# View status
run-git status

# View commit history
run-git log

# Branch operations
run-git branch              # List branches
run-git branch feature-x    # Create branch
run-git switch main         # Switch branch
run-git merge feature-x     # Merge branch

# Remote management
run-git remote              # Show remotes
run-git remote origin --add https://github.com/user/repo.git

# Advanced
run-git pull                # Pull changes
run-git sync                # Pull + Push
run-git stash               # Stash changes
run-git undo                # Undo last commit
```

---

## 🤖 Auto Commit Messages

RUN-GIT generates intelligent commit messages based on your changes:

- `feat: add authentication module (3 added)`
- `fix: update user validation (2 modified)`
- `docs: update README (1 modified)`
- `refactor: remove deprecated code (2 deleted)`

---

## 🎯 Use Cases

### For Beginners
- No need to remember complex Git commands
- Interactive menus guide you through operations
- Auto-generated commit messages

### For Experienced Developers
- Fast one-command push workflow
- Customizable commit messages
- Time-saving automation

---

## 📚 Command Reference

| Command | Description |
|---------|-------------|
| `run-git` | Interactive mode |
| `run-git push` | Quick push (add, commit, pull, push) |
| `run-git init` | Initialize repository |
| `run-git status` | Show repository status |
| `run-git log` | Show commit history |
| `run-git branch` | List branches |
| `run-git switch <name>` | Switch branch |
| `run-git merge <name>` | Merge branch |
| `run-git remote` | Show remotes |
| `run-git pull` | Pull changes |
| `run-git sync` | Pull and push |
| `run-git stash` | Stash changes |
| `run-git undo` | Undo last commit |
| `run-git --help` | Show help |
| `run-git --version` | Show version |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Himanshu Kumar**
- GitHub: [@himanshu231204](https://github.com/himanshu231204)
- Created with ❤️ for the developer community

---

## 🌟 Show Your Support

If you find RUN-GIT helpful, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest new features
- 🔀 Contribute code

---

## 📊 Why RUN-GIT?

### The Problem
Git is powerful but complex. Beginners struggle with:
- Remembering command sequences
- Handling merge conflicts
- Writing good commit messages
- Managing branches

### The Solution
RUN-GIT provides:
- ✅ One command for common workflows
- ✅ Interactive conflict resolution
- ✅ Auto-generated commit messages
- ✅ Beautiful terminal UI
- ✅ Safety features
- ✅ Zero learning curve

---

**Made with ❤️ by Himanshu Kumar | Making Git Easy for Everyone**