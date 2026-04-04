<!-- Context: documentation/api-reference | Priority: high | Version: 1.0 | Updated: 2026-04-05 -->

# RUN-GIT API Reference

> Complete CLI command reference for RUN-GIT.

## Quick Reference

| Category | Commands |
|----------|----------|
| **Core** | `push`, `status`, `log`, `sync` |
| **Branching** | `branch`, `switch`, `merge`, `delete` |
| **Remote** | `remote`, `pull`, `fetch` |
| **AI** | `commit-ai`, `pr-ai`, `review-ai`, `ai` |
| **GitHub** | `new`, `init` |
| **Utility** | `stash`, `undo`, `config` |

---

## Core Commands

### run-git (Interactive Mode)

Opens the interactive TUI menu. No memorization required.

```bash
run-git              # Open interactive menu
```

---

### run-git push

One-command workflow: add → commit → pull → push.

```bash
run-git push                        # Auto commit message + push
run-git push -m "feat: add login"  # Custom commit message
run-git push --dry-run             # Preview without executing
run-git push --force               # Force push (with confirmation)
```

**Options**:
| Flag | Description |
|------|-------------|
| `-m`, `--message` | Custom commit message |
| `--dry-run` | Preview changes without executing |
| `--force`, `-f` | Force push |
| `--no-commit` | Skip commit (add + push only) |
| `--amend` | Amend to last commit |

---

### run-git status

Show rich color-coded repository status.

```bash
run-git status          # Standard status
run-git status --short  # Compact output
```

**Output**: Staged, modified, untracked files in color-coded table

---

### run-git log

Show formatted commit history.

```bash
run-git log                    # Show last 10 commits
run-git log --max 20           # Show 20 commits
run-git log --oneline          # One line per commit
run-git log --graph            # ASCII branch graph
```

---

### run-git sync

Pull then push - keep local and remote in sync.

```bash
run-git sync           # Pull + Push
run-git sync --force   # Force sync
```

---

## Branching Commands

### run-git branch

List, create, or delete branches.

```bash
run-git branch              # List all branches
run-git branch feature-x   # Create new branch
run-git branch -d dev      # Delete branch
run-git branch -m old new  # Rename branch
```

---

### run-git switch

Switch to an existing branch.

```bash
run-git switch main        # Switch to main
run-git switch -c feature  # Create and switch
```

---

### run-git merge

Merge a branch into current branch.

```bash
run-git merge feature-x     # Merge feature-x into current
run-git merge feature-x --no-ff  # No fast-forward
```

---

## Remote Commands

### run-git remote

Manage git remotes.

```bash
run-git remote              # List remotes
run-git remote -v          # List with URLs
run-git remote add origin <url>   # Add remote
run-git remote remove origin     # Remove remote
```

---

### run-git pull

Pull latest changes from remote.

```bash
run-git pull              # Pull from default remote/branch
run-git pull origin main # Pull from specific
run-git pull --rebase    # Rebase instead of merge
```

---

### run-git fetch

Fetch from remote without merging.

```bash
run-git fetch              # Fetch all
run-git fetch origin main # Fetch specific
```

---

## AI Commands

### run-git commit-ai

Generate intelligent commit message using AI.

```bash
run-git commit-ai                    # Use staged changes
run-git commit-ai --unstaged          # Use all changes
run-git commit-ai --provider anthropic # Use specific provider
run-git commit-ai --model claude-3-5-sonnet  # Use specific model
```

**Options**:
| Flag | Description |
|------|-------------|
| `--unstaged` | Use unstaged changes instead of staged |
| `--provider` | AI provider (openai, anthropic, grok, google, local) |
| `--model` | Specific model to use |
| `--no-auto` | Skip auto-generation, use fallback |

**Output**: Conventional commit message with bullet points

---

### run-git pr-ai

Generate pull request description.

```bash
run-git pr-ai                              # Interactive PR creation
run-git pr-ai --base main --head feature   # Specify branches
run-git pr-ai --draft                      # Create as draft PR
```

**Output**: Structured PR description with Summary, Changes, Impact, Testing

---

### run-git review-ai

Get AI-powered code review.

```bash
run-git review-ai                  # Review staged changes
run-git review-ai --uncommitted    # Review all changes
run-git review-ai --provider anthropic  # Use specific provider
```

**Output categories**:
- Bugs (⚠️)
- Code Quality Issues (💡)
- Performance Issues (🚀)
- Best Practices (📌)

---

### run-git ai

OpenAI assistant mode - chat with AI about your code.

```bash
run-git ai                    # Interactive chat mode
run-git ai "explain this"     # Single query
run-git ai --context code     # Use code as context
```

---

## GitHub Commands

### run-git new

Create a new GitHub repository.

```bash
run-git new my-project                       # Interactive wizard
run-git new my-project --quick              # Use defaults
run-git new my-api -d "REST API" --public  # With options
```

**Options**:
| Flag | Description |
|------|-------------|
| `-d`, `--description` | Repository description |
| `--public` | Public repository |
| `--private` | Private repository |
| `-g`, `--gitignore` | Language for .gitignore |
| `-l`, `--license` | License (MIT, GPL, etc.) |
| `--quick` | Skip prompts, use defaults |
| `--no-git` | Don't initialize git |
| `--remote` | Add remote to existing repo |

---

### run-git init

Initialize a local repository or clone an existing one.

```bash
run-git init                    # Initialize new repo
run-git init https://github.com/user/repo.git  # Clone
run-git init my-repo --github   # Create + GitHub
```

---

## Utility Commands

### run-git stash

Stash uncommitted changes.

```bash
run-git stash              # Stash all changes
run-git stash save "msg"  # Stash with message
run-git stash list        # List stashes
run-git stash pop         # Apply and remove latest
run-git stash apply       # Apply without removing
run-git stash drop        # Delete stash
```

---

### run-git undo

Undo the last commit (keeps changes staged).

```bash
run-git undo              # Undo last commit
run-git undo --hard       # Also discard changes (dangerous)
run-git undo 3           # Undo last 3 commits
```

---

### run-git config

Manage configuration.

```bash
run-git config                    # Show all config
run-git config --list             # List settings
run-git config ai.provider        # Get specific value
run-git config ai.provider openai # Set value
run-git config --global           # Edit global config
run-git config --edit            # Open in editor
```

---

## Stacked Commands

### run-git graph

Visual commit history with branch visualization.

```bash
run-git graph              # Table view (default)
run-git graph --graph      # ASCII branch graph
run-git graph --oneline   # Compact graph
run-git graph -n 20       # Last 20 commits
```

---

### run-git theme

Customize terminal appearance.

```bash
run-git theme                   # List themes
run-git theme set dark          # Set dark theme
run-git theme set light        # Set light theme
run-git theme preview         # Preview all themes
```

---

## Global Options

These options work with all commands:

```bash
run-git --version              # Show version
run-git --help                 # Show help
run-git --verbose             # Verbose output
run-git --quiet               # Minimal output
run-git --color {auto,always,never}  # Color control
```

---

## Configuration File

Location: `~/.config/run-git/config.yaml`

**Example**:
```yaml
ai:
  provider: openai
  model: gpt-4o
  temperature: 0.7

github:
  default_remote: origin
  default_branch: main

defaults:
  push_on_sync: true
  auto_stash: true

theme: dark
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `RUN_GIT_CONFIG` | Custom config file path |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GROK_API_KEY` | xAI API key |
| `GOOGLE_API_KEY` | Google AI API key |
| `GITHUB_TOKEN` | GitHub personal access token |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Not a git repository |
| 3 | No changes to commit |
| 4 | Merge conflict |
| 5 | Authentication error |
| 126 | Command not found |
| 127 | Invalid arguments |

---

## Related Files

- `README.md` - Quick start guide
- `QUICKSTART.md` - 2-minute tutorial
- `INSTALL.md` - Installation guide
- `ARCHITECTURE.md` - Technical architecture
