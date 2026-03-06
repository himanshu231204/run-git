# GITPUSH - Git Made Easy 🚀

```
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃                                                                    ┃
┃    ██████╗ ██╗████████╗██████╗ ██╗   ██╗███████╗██╗  ██╗         ┃
┃   ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██╔════╝██║  ██║         ┃
┃   ██║  ███╗██║   ██║   ██████╔╝██║   ██║███████╗███████║         ┃
┃   ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║╚════██║██╔══██║         ┃
┃   ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████║██║  ██║         ┃
┃    ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝         ┃
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
┃   Type 'gitpush help' to get started                              ┃
┃                                                                    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
```

[![PyPI version](https://badge.fury.io/py/gitpush.svg)](https://badge.fury.io/py/gitpush)
[![Tests](https://github.com/himanshu231204/gitpush/workflows/Tests/badge.svg)](https://github.com/himanshu231204/gitpush/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**One Command To Rule Them All**

GITPUSH is the ultimate Git automation tool designed to make Git operations effortless for developers of all skill levels. Say goodbye to complex Git commands and hello to simplicity!

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
pip install gitpush
```

---

## 🚀 Quick Start

### 1. Initialize Repository
```bash
# New repository
gitpush init

# Clone existing repository
gitpush init https://github.com/user/repo.git
```

### 2. Quick Push (Most Common Use Case)
```bash
# Add, commit, pull, and push in one command!
gitpush push

# With custom commit message
gitpush push -m "Add new feature"
```

### 3. Interactive Mode
```bash
# Just type gitpush for interactive menu
gitpush
```

---

## 📖 Usage

### Basic Commands

```bash
# Push changes
gitpush push

# View status
gitpush status

# View commit history
gitpush log

# Branch operations
gitpush branch              # List branches
gitpush branch feature-x    # Create branch
gitpush switch main         # Switch branch
gitpush merge feature-x     # Merge branch

# Remote management
gitpush remote              # Show remotes
gitpush remote origin --add https://github.com/user/repo.git

# Advanced
gitpush pull                # Pull changes
gitpush sync                # Pull + Push
gitpush stash               # Stash changes
gitpush undo                # Undo last commit
```

---

## 🤖 Auto Commit Messages

GITPUSH generates intelligent commit messages based on your changes:

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
| `gitpush` | Interactive mode |
| `gitpush push` | Quick push (add, commit, pull, push) |
| `gitpush init` | Initialize repository |
| `gitpush status` | Show repository status |
| `gitpush log` | Show commit history |
| `gitpush branch` | List branches |
| `gitpush switch <n>` | Switch branch |
| `gitpush merge <n>` | Merge branch |
| `gitpush remote` | Show remotes |
| `gitpush pull` | Pull changes |
| `gitpush sync` | Pull and push |
| `gitpush stash` | Stash changes |
| `gitpush undo` | Undo last commit |
| `gitpush --help` | Show help |
| `gitpush --version` | Show version |

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

If you find GITPUSH helpful, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest new features
- 🔀 Contribute code

---

## 📊 Why GITPUSH?

### The Problem
Git is powerful but complex. Beginners struggle with:
- Remembering command sequences
- Handling merge conflicts
- Writing good commit messages
- Managing branches

### The Solution
GITPUSH provides:
- ✅ One command for common workflows
- ✅ Interactive conflict resolution
- ✅ Auto-generated commit messages
- ✅ Beautiful terminal UI
- ✅ Safety features
- ✅ Zero learning curve

---

**Made with ❤️ by Himanshu Kumar | Making Git Easy for Everyone**
