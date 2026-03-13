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
┃   │  Version      : v1.0.5                                   │   ┃
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
- 🆕 **GitHub Repo Creation**: Create repositories directly from command line (NEW!)

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

### 4. 🆕 Create GitHub Repository (NEW!)
```bash
# Create a new repo with smart defaults
run-git new my-awesome-project --quick

# Interactive mode with all options
run-git new my-project
```

---

## 🆕 NEW Feature: GitHub Repository Creation

Create GitHub repositories directly from your terminal without opening a browser!

### ⚙️ One-Time Setup

Before using `run-git new`, you need a GitHub Personal Access Token (only once):

#### **Step 1: Create GitHub Token**

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name: `run-git-token`
4. Select scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **user** (Read user profile data)
5. Click **"Generate token"**
6. **Copy the token** (starts with `ghp_...`)
   ⚠️ You won't see it again!

#### **Step 2: First Time Use**

```bash
run-git new my-first-repo --quick
```

You'll be prompted:
```
ℹ️  GitHub Personal Access Token needed!
ℹ️  Create one at: https://github.com/settings/tokens
ℹ️  Required scopes: repo, user
? Enter your GitHub token: 
```

**Paste your token** (won't show while typing) and press Enter.

```
✅ Authenticated as: your-username
✅ GitHub token saved securely
```

**That's it!** Your token is now saved. You'll never be asked again! 🎉

#### **Token Storage**

Token is securely stored in:
- **Linux/Mac**: `~/.run-git/config.yml`
- **Windows**: `C:\Users\YourName\.run-git\config.yml`

File permissions are set to user-only (600) for security.

---

### 💡 Using run-git new

#### **Quick Mode (Recommended for Speed)**
```bash
# Create repo with smart defaults
run-git new my-awesome-project --quick
```

**What it does:**
- ✅ Detects language from your files (Python, Node, Java, etc.)
- ✅ Creates .gitignore automatically
- ✅ Adds MIT license
- ✅ Generates professional README
- ✅ Makes repository public
- ✅ Pushes to GitHub
- ✅ All in 5 seconds!

#### **Interactive Mode (Full Control)**
```bash
# Answer questions for each option
run-git new my-project
```

You'll be asked:
- Repository description
- Public or Private
- Gitignore template (160+ languages supported!)
- License (MIT, Apache, GPL, BSD, etc.)
- Create README?

#### **Command Line Options**
```bash
# Specify everything upfront
run-git new my-api \
  --description "REST API for my app" \
  --public \
  --gitignore Python \
  --license MIT
```

### 📋 Available Options

| Option | Description |
|--------|-------------|
| `--quick` | Use smart defaults, no prompts |
| `-d, --description` | Repository description |
| `--public` | Make repository public (default) |
| `--private` | Make repository private |
| `-g, --gitignore` | Gitignore template (Python, Node, Java, etc.) |
| `-l, --license` | License (MIT, Apache-2.0, GPL-3.0, BSD, ISC) |
| `--no-readme` | Skip README creation |

### 🎬 Example Workflow

```bash
# Create new project folder
mkdir my-web-app
cd my-web-app

# Add some files
echo "print('Hello')" > app.py
echo "flask" > requirements.txt

# Create repo (auto-detects Python!)
run-git new my-web-app --quick
```

**Output:**
```
✅ Using smart defaults...
ℹ️  Language detected: Python
ℹ️  License: MIT
ℹ️  Visibility: Public
⏳ Creating repository on GitHub...
✅ Repository created: https://github.com/you/my-web-app
✅ .gitignore (Python) created
✅ LICENSE (MIT) created
✅ README.md created
✅ Pushed to GitHub
🎉 Repository created successfully!
🔗 https://github.com/you/my-web-app
```

**Your repo is LIVE on GitHub!** 🚀

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
- Create GitHub repos without leaving terminal

### For Experienced Developers
- Fast one-command push workflow
- Customizable commit messages
- Time-saving automation
- Quick repo creation for new projects

---

## 📚 Command Reference

| Command | Description |
|---------|-------------|
| `run-git` | Interactive mode |
| `run-git push` | Quick push (add, commit, pull, push) |
| `run-git new <n>` | 🆕 Create new GitHub repository |
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

### Token Issues

**Q: I lost my token, how do I create a new one?**

A: Delete the saved token and run any `run-git new` command:
```bash
# Linux/Mac
rm ~/.run-git/config.yml

# Windows
del %USERPROFILE%\.run-git\config.yml

# Then run
run-git new test-repo --quick
```

**Q: How do I update my token?**

A: Same as above - delete the config file and enter a new token.

**Q: Is my token secure?**

A: Yes! The token is:
- Stored locally on your machine only
- File permissions set to user-only (600)
- Never transmitted except to GitHub's official API
- Can be revoked anytime from GitHub settings

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
- Creating GitHub repositories

### The Solution
RUN-GIT provides:
- ✅ One command for common workflows
- ✅ Interactive conflict resolution
- ✅ Auto-generated commit messages
- ✅ Beautiful terminal UI
- ✅ Safety features
- ✅ Zero learning curve
- ✅ 🆕 One-command GitHub repo creation

---

## 📈 What's New in v1.0.4

### 🆕 New Features
- **GitHub Repository Creation**: Create repos from terminal with `run-git new`
- **Smart Language Detection**: Auto-detects Python, Node, Java, Go, Rust, and 160+ languages
- **Auto .gitignore**: Generates language-specific .gitignore files
- **License Support**: MIT, Apache, GPL, BSD, ISC licenses
- **One-time Token Setup**: Secure token storage for seamless workflow

### 🐛 Bug Fixes
- Improved error handling
- Better token validation
- Enhanced cross-platform compatibility

### 🔧 Improvements
- Faster repository creation
- Better user prompts
- Improved documentation

---

**Made with ❤️ by Himanshu Kumar | Making Git Easy for Everyone**