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
┃   │  Version      : v1.0.7                                   │   ┃
┃   │  License      : MIT                                      │   ┃
┃   └──────────────────────────────────────────────────────────┘   ┃
┃                                                                    ┃
┃   Type 'run-git help' to get started                              ┃
┃                                                                    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
```

[![PyPI version](https://badge.fury.io/py/run-git.svg)](https://badge.fury.io/py/run-git)
[![Downloads](https://static.pepy.tech/badge/run-git)](https://pepy.tech/project/run-git)
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
- 🆕 **GitHub Repo Creation**: Create repositories from CLI or interactive menu
- 📂 **Smart Folder Detection**: Automatically detects existing files and asks for confirmation
- 🔄 **Existing Repo Support**: Connect existing local repos to GitHub
- 🔧 **Intelligent Remote Management**: Handles existing remotes gracefully
- 🚀 **Enhanced Push Reliability**: Fixed URL issues, token auth, auto-retry

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

**New in v1.0.7:** Smart folder detection and existing repo support! 🎉

---

## 🆕 v1.0.7: Smart Repository Creation

### 🎯 What's New

#### **1. Smart Folder Detection** 📂

RUN-GIT now detects existing files before creating a repository!

```bash
cd my-existing-project  # Folder with existing files

run-git
# Select "🆕 Create New Repo"
```

**Output:**
```
📂 Found 10 file(s) in current folder:
   • app.py
   • requirements.txt
   • config.json
   • utils.py
   • models.py
   ... and 5 more

? Create repository and include these files? (Y/n)
```

**Benefits:**
- ✅ See what files will be included
- ✅ Prevent accidental commits
- ✅ Full transparency before creating repo

#### **2. Existing Repository Support** 🔄

Already have a local git repo? Connect it to GitHub!

```bash
cd my-git-project  # Already initialized with git

run-git
# Select "🆕 Create New Repo"
```

**Output:**
```
⚠️  This directory is already a git repository!
ℹ️  Remote: None

? Connect this existing local repo to new GitHub repository? (Y/n)
```

**Benefits:**
- ✅ Preserves existing git history
- ✅ Connects to new GitHub repo
- ✅ No need to re-initialize

#### **3. Smart Remote Management** 🔗

Handles existing remotes intelligently!

```
⚠️  Remote 'origin' already exists

? Replace existing remote 'origin' with new repository? (Y/n)
```

**Benefits:**
- ✅ Never accidentally overwrites remotes
- ✅ Clear confirmation before changes
- ✅ Option to keep existing setup

#### **4. File Conflict Prevention** 📄

Never overwrites your existing files!

```
ℹ️  .gitignore already exists, skipping...
ℹ️  LICENSE already exists, skipping...
ℹ️  README.md already exists, skipping...
```

**Benefits:**
- ✅ Preserves your custom configurations
- ✅ Clear messages about what's skipped
- ✅ Safe operations always

#### **5. Fixed Push Issues** 🔧

Resolved "protocol 'https' is not supported" error!

**What was fixed:**
- ✅ Clean URL formatting (removes invisible characters)
- ✅ Token-based authentication
- ✅ Better Windows compatibility
- ✅ Enhanced error messages

---

## 💡 Use Cases

### **Scenario 1: New Empty Project**
```bash
mkdir new-app
cd new-app
run-git new my-app --quick
```
**Result:** Fresh repo with all files! ✅

### **Scenario 2: Existing Project with Files**
```bash
cd my-existing-app  # Has 20 files
run-git
# Select "Create New Repo"
# Confirms: "Found 20 files, include them?"
# You: Yes
```
**Result:** All files pushed to new GitHub repo! ✅

### **Scenario 3: Already a Git Repo (No Remote)**
```bash
cd my-git-project  # Already has .git
run-git
# "Connect existing repo to GitHub?"
# You: Yes
```
**Result:** Existing repo connected to GitHub! ✅

### **Scenario 4: Has Remote Already**
```bash
cd project-with-remote
run-git
# "Replace existing remote?"
# You: Yes/No
```
**Result:** Handled gracefully! ✅

---

## 🆕 GitHub Repository Creation

### ⚙️ One-Time Setup

**Step 1: Create GitHub Token**

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `run-git-token`
4. Scopes: ✅ **repo** + ✅ **user**
5. Generate and copy token

**Step 2: First Time Use**

```bash
run-git new my-first-repo --quick
```

Paste token when prompted. **Saved forever!** 🎉

---

### 💡 Creating Repositories

#### **Method 1: Interactive Menu** (Recommended)

```bash
run-git
```

Select **"🆕 Create New Repo"**

**Features:**
- 📂 Shows existing files
- 🔄 Handles existing repos
- 🔗 Manages remotes
- ✅ Confirms every step

#### **Method 2: CLI Quick Mode**
```bash
run-git new my-project --quick
```

#### **Method 3: CLI Interactive**
```bash
run-git new my-project
```

#### **Method 4: Full Command**
```bash
run-git new my-api -d "REST API" --public -g Python -l MIT
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

# Advanced
run-git pull                # Pull changes
run-git sync                # Pull + Push
run-git stash               # Stash changes
run-git undo                # Undo last commit
```

---

## 🤖 Auto Commit Messages

RUN-GIT generates intelligent commit messages:

- `feat: add authentication module (3 added)`
- `fix: update user validation (2 modified)`
- `docs: update README (1 modified)`
- `refactor: remove deprecated code (2 deleted)`

---

## 📚 Command Reference

| Command | Description |
|---------|-------------|
| `run-git` | Interactive mode with Create Repo |
| `run-git push` | Quick push (add, commit, pull, push) |
| `run-git new <n>` | Create new GitHub repository |
| `run-git init` | Initialize repository |
| `run-git status` | Show repository status |
| `run-git log` | Show commit history |
| `run-git branch` | List branches |
| `run-git switch <n>` | Switch branch |
| `run-git merge <n>` | Merge branch |
| `run-git remote` | Show remotes |
| `run-git pull` | Pull changes |
| `run-git sync` | Pull and push |
| `run-git stash` | Stash changes |
| `run-git undo` | Undo last commit |
| `run-git --help` | Show help |
| `run-git --version` | Show version |

---

## 🔧 Troubleshooting

### Common Issues

**Q: "protocol 'https' is not supported" error?**

A: **Fixed in v1.0.7!** Update to latest version:
```bash
pip install --upgrade run-git
```

**Q: Push fails after repo creation?**

A: v1.0.7 includes automatic retry with token authentication. Should work now!

**Q: Already have files in folder?**

A: v1.0.7 detects them and asks for confirmation. Safe to use!

**Q: Already a git repo?**

A: v1.0.7 can connect it to GitHub. Just confirm when asked!

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

## 📈 What's New in v1.0.7

### 🆕 Major Features
- **Smart Folder Detection**: See existing files before creating repo
- **Existing Repo Support**: Connect local repos to GitHub
- **Smart Remote Management**: Handle existing remotes gracefully
- **File Conflict Prevention**: Never overwrites existing files

### 🔧 Critical Fixes
- **Fixed "protocol 'https' is not supported" error**
- Better URL handling with whitespace removal
- Token-based push authentication
- Enhanced error recovery

### 🎯 Improvements
- Context-aware commit messages
- Better user confirmations
- Clearer progress messages
- More robust push mechanism

### 🐛 Bug Fixes
- Fixed push failures on Windows
- Fixed URL malformation issues
- Better handling of existing git repos
- Improved remote conflict resolution

---

## 📊 Why RUN-GIT?

### The Problem
Git is powerful but complex. Developers struggle with:
- Remembering command sequences
- Handling merge conflicts
- Writing good commit messages
- Managing branches
- Creating GitHub repositories
- Dealing with existing projects
- Push failures and errors

### The Solution
RUN-GIT provides:
- ✅ One command for common workflows
- ✅ Interactive menus for guidance
- ✅ Auto-generated commit messages
- ✅ Beautiful terminal UI
- ✅ Smart folder detection
- ✅ Existing repo support
- ✅ Automatic error recovery
- ✅ Zero learning curve

---

**Made with ❤️ by Himanshu Kumar | Making Git Easy for Everyone**