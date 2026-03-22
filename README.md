<div align="center">

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
┃              ⚡ Git Operations Made Effortless ⚡                  ┃
┃          One Command · Zero Hassle · Full Control                 ┃
┃                                                                    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
```

[![PyPI version](https://badge.fury.io/py/run-git.svg)](https://badge.fury.io/py/run-git)
[![Downloads](https://static.pepy.tech/badge/run-git)](https://pepy.tech/project/run-git)
[![Tests](https://github.com/himanshu231204/gitpush/workflows/Tests/badge.svg)](https://github.com/himanshu231204/gitpush/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI - Status](https://img.shields.io/pypi/status/run-git)](https://pypi.org/project/run-git/)
[![GitHub Stars](https://img.shields.io/github/stars/himanshu231204/gitpush)](https://github.com/himanshu231204/gitpush/stargazers)

### Stop memorising Git commands. Start shipping code.

**RUN-GIT** is a Python-powered CLI that wraps Git's most common workflows into a single, intuitive command — with auto commit messages, interactive menus, branch management, GitHub repo creation, and more. Perfect for students, hackathon builders, and any developer who wants to move fast without friction.

[📦 Install](#-installation) · [🚀 Quick Start](#-quick-start) · [📖 Commands](#-command-reference) · [🤝 Contribute](#-contributing)

</div>

---

## ✨ Why RUN-GIT?

Tired of typing four commands every time you want to save your work?

```bash
# The old way — every single time
git add .
git commit -m "update"
git pull origin main
git push origin main

# The RUN-GIT way
run-git push
```

That's it. One command does all four steps, auto-generates a meaningful commit message, handles conflicts, and pushes — safely.

---

## 🎯 Features

| Feature | Description |
|---|---|
| ⚡ **One-Command Push** | `run-git push` does add → commit → pull → push automatically |
| 🤖 **Smart Commit Messages** | Auto-generates Conventional Commits style messages based on your changes |
| 🎨 **Interactive TUI** | Full terminal menu — no flags to remember |
| 🆕 **GitHub Repo Creator** | Create public/private repos from the CLI without leaving your terminal |
| 🌿 **Branch Management** | Create, switch, merge, and delete branches with simple commands |
| 🔐 **Secret File Guard** | Warns you before accidentally pushing `.env`, tokens, or credentials |
| 🔀 **Conflict Helper** | Guided, interactive merge-conflict resolution |
| 🔄 **Smart Sync** | Pull + push in one step, with auto-retry on failure |
| 📊 **Rich Status View** | Colour-coded, table-based status output powered by Rich |
| 🔧 **Remote Management** | Intelligently handles existing remotes and URL mismatches |

---

## 📦 Installation

```bash
pip install run-git
```

Requires **Python 3.8+**. Works on macOS, Linux, and Windows.

> First time? Set your GitHub token once with `run-git init` and you're ready to go.

---

## 🚀 Quick Start

### Push your changes (most common workflow)
```bash
run-git push                        # auto commit message + push
run-git push -m "feat: add login"   # custom commit message
```

### Launch the interactive menu
```bash
run-git          # full TUI — no commands to memorise
```

### Create a new GitHub repository
```bash
run-git new my-project                              # guided wizard
run-git new my-project --quick                      # sensible defaults, no prompts
run-git new my-api -d "REST API" --public -g Python -l MIT   # full control
```

### Initialise a repository
```bash
run-git init                                    # new local repo
run-git init https://github.com/user/repo.git  # clone existing repo
```

---

## 📖 Command Reference

| Command | Description |
|---------|-------------|
| `run-git` | Open the interactive TUI menu |
| `run-git push` | Add, commit, pull, and push in one step |
| `run-git push -m "<msg>"` | Push with a custom commit message |
| `run-git new <name>` | Create a new GitHub repository |
| `run-git init` | Initialise a local or cloned repository |
| `run-git status` | Rich colour-coded repository status |
| `run-git log` | Formatted commit history |
| `run-git branch` | List all branches |
| `run-git branch <name>` | Create a new branch |
| `run-git switch <name>` | Switch to a branch |
| `run-git merge <name>` | Merge a branch into the current one |
| `run-git pull` | Pull latest changes |
| `run-git sync` | Pull then push (keep in sync) |
| `run-git remote` | Show configured remotes |
| `run-git stash` | Stash uncommitted changes |
| `run-git undo` | Undo the last commit (keeps changes staged) |
| `run-git --version` | Show installed version |
| `run-git --help` | Show help for any command |

---

## 🤖 Auto Commit Messages

RUN-GIT analyses your staged changes and generates [Conventional Commits](https://www.conventionalcommits.org/) style messages automatically:

```
feat: add authentication module (3 files added)
fix: update user validation logic (2 files modified)
docs: update README and contributing guide (1 file modified)
refactor: remove deprecated helper functions (2 files deleted)
```

No more `git commit -m "stuff"` or `git commit -m "fix"`.

---

## 🆚 How Does It Compare?

| | Raw Git | GitHub CLI (`gh`) | **RUN-GIT** |
|---|---|---|---|
| Push in one command | ❌ | ❌ | ✅ |
| Auto commit messages | ❌ | ❌ | ✅ |
| Interactive TUI menu | ❌ | Partial | ✅ |
| Create GitHub repos | ❌ | ✅ | ✅ |
| Secret file warnings | ❌ | ❌ | ✅ |
| Learning curve | High | Medium | **Zero** |

> RUN-GIT is a *speed layer* on top of Git — not a replacement. Use it for daily work; reach for `git` or `gh` when you need fine-grained control.

---

## 💡 Who Is It For?

- 🎓 **Students & beginners** learning Git without drowning in flags
- 🚀 **Hackathon builders** who need to ship fast
- ⚡ **Indie developers** doing solo projects with quick iteration cycles
- 🔁 **Any developer** who runs the same four Git commands dozens of times a day

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are all welcome!
Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

```bash
git clone https://github.com/himanshu231204/gitpush.git
cd gitpush
pip install -e ".[test]"
pytest
```

---

## 📝 License

Distributed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Himanshu Kumar** — [@himanshu231204](https://github.com/himanshu231204)

Built with ❤️ to make every developer's Git life a little simpler.

---

<div align="center">

**If RUN-GIT saves you time, please consider giving it a ⭐ — it helps others find the project!**

[![Star History Chart](https://api.star-history.com/svg?repos=himanshu231204/gitpush&type=Date)](https://star-history.com/#himanshu231204/gitpush&Date)

</div>
