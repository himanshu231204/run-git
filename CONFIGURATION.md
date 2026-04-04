<!-- Context: documentation/configuration | Priority: high | Version: 1.0 | Updated: 2026-04-05 -->

# RUN-GIT Configuration Guide

> Complete configuration reference for RUN-GIT.

## Quick Reference

- **Purpose**: Configure RUN-GIT behavior
- **Update When**: Changing settings or setting up
- **Audience**: Users, developers

---

## Configuration Files

### User Config

Location: `~/.config/run-git/config.yaml`

### Project Config

Location: `.run-git.yaml` (project root)

### Priority

1. Project config (highest)
2. User config
3. Environment variables
4. Defaults (lowest)

---

## Config File Format

### YAML Structure

```yaml
ai:
  provider: openai
  model: gpt-4o
  temperature: 0.7

github:
  token: ${GITHUB_TOKEN}

defaults:
  branch: main
  remote: origin

theme: dark

features:
  auto_stash: true
  secret_warnings: true
```

---

## AI Settings

### Provider Selection

```yaml
ai:
  provider: openai          # openai, anthropic, grok, google, local
  model: gpt-4o            # Model name
  temperature: 0.7         # 0.0-1.0 (creativity)
  max_tokens: 2000         # Response limit
```

### Provider Options

| Provider | Models |
|----------|--------|
| `openai` | gpt-4o, gpt-4, gpt-3.5-turbo |
| `anthropic` | claude-3-5-sonnet, claude-3-opus |
| `grok` | grok-2, grok-2-vision |
| `google` | gemini-2.0-flash, gemini-1.5-pro |
| `local` | ollama/*, lmstudio/* |

### API Keys

```yaml
ai:
  # Option 1: Environment variable (recommended)
  api_key: ${OPENAI_API_KEY}

  # Option 2: Direct (not recommended)
  api_key: sk-xxxxxxxxxxxx
```

---

## GitHub Settings

### Token Configuration

```yaml
github:
  token: ${GITHUB_TOKEN}    # GitHub PAT
  default_remote: origin
  default_branch: main
```

### Create Token

1. Go to GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token with `repo` scope

---

## Default Settings

### Branch Defaults

```yaml
defaults:
  branch: main             # Default branch name
  remote: origin           # Default remote name
  push_on_sync: true      # Auto-push on sync
```

### Behavior

```yaml
defaults:
  auto_stash: true        # Stash before operations
  pull_before_push: true  # Pull before push
  force_on_sync: false    # Force sync
  dry_run: false          # Dry run default
```

---

## Theme Settings

### Available Themes

```yaml
theme: dark              # dark, light, auto
```

### Custom Colors

```yaml
theme:
  primary: "#00FF00"     # Primary color
  secondary: "#FFFFFF"   # Secondary color
  error: "#FF0000"       # Error color
  success: "#00FF00"     # Success color
```

---

## Feature Flags

### Enable/Disable Features

```yaml
features:
  secret_warnings: true      # Warn about .env, secrets
  interactive_conflicts: true # Interactive conflict resolution
  auto_commit: true         # Auto-generate commit messages
  pretty_log: true          # Pretty log format
  graph_output: true        # Graph visualization
```

---

## Environment Variables

### API Keys

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GROK_API_KEY` | xAI API key |
| `GOOGLE_API_KEY` | Google AI API key |
| `GITHUB_TOKEN` | GitHub personal access token |

### RUN-GIT Settings

| Variable | Description |
|----------|-------------|
| `RUN_GIT_CONFIG` | Custom config file path |
| `RUN_GIT_DEBUG` | Enable debug mode |

---

## Command Options

### Override Config

```bash
# Override provider
run-git commit-ai --provider anthropic

# Override model
run-git commit-ai --model claude-3-5-sonnet

# Dry run
run-git push --dry-run
```

---

## Using Config Command

### View Config

```bash
run-git config              # Show all
run-git config --list      # List settings
run-git config ai.provider # Get specific
```

### Set Config

```bash
run-git config ai.provider openai
run-git config theme dark
run-git config defaults.branch main
```

### Edit Config File

```bash
run-git config --edit      # Open in editor
run-git config --global    # Edit global config
```

---

## Config Templates

### Minimal

```yaml
github:
  token: ${GITHUB_TOKEN}
```

### Full

```yaml
ai:
  provider: openai
  model: gpt-4o
  temperature: 0.7
  api_key: ${OPENAI_API_KEY}

github:
  token: ${GITHUB_TOKEN}
  default_remote: origin
  default_branch: main

defaults:
  branch: main
  remote: origin
  push_on_sync: true
  auto_stash: true

theme: dark

features:
  secret_warnings: true
  interactive_conflicts: true
  auto_commit: true
```

---

## Related Files

- `cli.py` - CLI entry point
- `config/settings.py` - Settings management
- `API_REFERENCE.md` - Command reference
