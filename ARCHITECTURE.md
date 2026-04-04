<!-- Context: project-intelligence/technical | Priority: critical | Version: 1.1 | Updated: 2026-04-05 -->

# RUN-GIT Architecture

> Technical architecture, components, and design decisions for RUN-GIT CLI.

## Quick Reference

- **Purpose**: Understand how RUN-GIT is structured technically
- **Update When**: Adding features, refactoring, or understanding codebase
- **Audience**: Developers, contributors, AI agents

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Entry Point                      │
│                           cli.py                             │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     ┌──────────┐      ┌──────────┐      ┌──────────┐
     │commands/ │      │   core/   │      │    ai/   │
     │  (thin)  │      │ (logic)  │      │ (AI ops) │
     └──────────┘      └──────────┘      └──────────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                        ┌──────────┐
                        │   ui/    │
                        │ (Rich)   │
                        └──────────┘
```

---

## Directory Structure

```
gitpush/
├── cli.py                    # Main CLI entry (Click group)
├── commands/                 # Thin orchestration layer
│   ├── push.py              # Push workflow
│   ├── init.py              # Repository init
│   ├── status.py            # Status & log
│   ├── branch.py            # Branch operations
│   ├── github.py            # GitHub API
│   ├── graph.py             # Commit visualization
│   ├── commit_ai.py         # AI commit messages
│   ├── pr_ai.py             # AI PR descriptions
│   ├── review_ai.py         # AI code review
│   └── ...
├── core/                     # Business logic (testable)
│   ├── git_operations.py    # Git operations wrapper
│   ├── commit_generator.py  # Auto message generation
│   ├── conflict_resolver.py # Merge conflict handling
│   ├── graph_renderer.py    # ASCII graph rendering
│   ├── github_manager.py    # GitHub API wrapper
│   └── ai_engine.py         # AI orchestration
├── ai/                       # AI layer
│   ├── client.py            # Unified AI client
│   ├── factory.py           # Provider selector
│   ├── config.py            # AI configuration
│   ├── prompts/             # Prompt templates
│   │   ├── commit_prompt.py
│   │   ├── pr_prompt.py
│   │   └── review_prompt.py
│   └── providers/           # AI provider implementations
│       ├── openai.py
│       ├── anthropic.py
│       ├── grok.py
│       ├── google.py
│       └── local.py
├── ui/                       # Terminal UI (Rich)
│   ├── banner.py            # ASCII banners
│   └── interactive.py       # Interactive menus
├── utils/                    # Utilities
│   ├── validators.py        # Input validation
│   ├── formatters.py        # Output formatting
│   ├── file_helpers.py      # File operations
│   ├── diff_cleaner.py      # Git diff cleaning
│   └── license.py           # License display
├── config/                   # Configuration
│   └── settings.py          # Settings management
└── exceptions.py            # Custom exceptions
```

---

## Core Components

### 1. CLI Layer (`cli.py`)

**Responsibilities**:
- Parse command-line arguments
- Route to appropriate command handlers
- Display help and version

**Technology**: Click framework

**Key patterns**:
- `@cli.command()` decorators for each command
- Context objects for shared state
- Error handling with custom exceptions

---

### 2. Commands Layer (`commands/`)

**Design principle**: Thin orchestration - parse args, call core, render output.

**Each command module**:
```python
# Minimal pattern
@click.command()
@click.options(...)
def command_name(ctx, ...):
    # 1. Parse arguments
    # 2. Call core service
    # 3. Render output via UI
    pass
```

**Commands**:
| Command | Purpose |
|---------|---------|
| `push.py` | Add → commit → pull → push workflow |
| `init.py` | Initialize/clone repository |
| `status.py` | Rich status display |
| `branch.py` | Branch CRUD operations |
| `github.py` | GitHub repository creation |
| `graph.py` | Commit history visualization |
| `commit_ai.py` | AI-generated commit messages |
| `pr_ai.py` | AI-generated PR descriptions |
| `review_ai.py` | AI-powered code review |

---

### 3. Core Layer (`core/`)

**Design principle**: Pure business logic, no CLI dependencies.

**Modules**:

| Module | Responsibility |
|--------|----------------|
| `git_operations.py` | Git operations (add, commit, push, pull, etc.) |
| `commit_generator.py` | Generate Conventional Commits messages |
| `conflict_resolver.py` | Interactive merge conflict resolution |
| `graph_renderer.py` | ASCII commit graph generation |
| `github_manager.py` | GitHub API operations |
| `ai_engine.py` | Orchestrate AI operations |

**Key patterns**:
- All functions are pure/testable
- Return structured data, not formatted strings
- Raise custom exceptions on failure

---

### 4. AI Layer (`ai/`)

**Purpose**: Unified AI integration for commit messages, PR descriptions, and code reviews.

**Components**:

```
ai/
├── client.py         # Main client - send requests
├── factory.py        # Provider factory (OpenAI, Anthropic, etc.)
├── config.py         # Configuration management
├── prompts/          # Prompt templates
│   ├── commit_prompt.py
│   ├── pr_prompt.py
│   └── review_prompt.py
└── providers/        # Provider implementations
    ├── base.py       # Base provider class
    ├── openai.py    # OpenAI provider
    ├── anthropic.py # Anthropic provider
    ├── grok.py      # xAI Grok provider
    ├── google.py    # Google AI provider
    └── local.py     # Local/Ollama provider
```

**Supported providers**:
- OpenAI (GPT-4, GPT-4o)
- Anthropic (Claude)
- xAI (Grok)
- Google (Gemini)
- Local (Ollama, LM Studio)

---

### 5. UI Layer (`ui/`)

**Technology**: Rich library for terminal output

**Components**:
| Component | Purpose |
|-----------|---------|
| `banner.py` | ASCII art banners and branding |
| `interactive.py` | Interactive TUI menus |

**Features**:
- Color-coded output
- Tables and panels
- Progress indicators
- Interactive prompts

---

### 6. Utils Layer (`utils/`)

**Modules**:
| Module | Purpose |
|--------|---------|
| `validators.py` | Input validation |
| `formatters.py` | Output formatting |
| `file_helpers.py` | File operations |
| `diff_cleaner.py` | Clean git diff output |
| `license.py` | License display |

---

## Data Flow

### Typical Command Flow

```
1. User types command
   ↓
2. cli.py parses args with Click
   ↓
3. Command module (commands/push.py)
   ├─ Parse additional options
   ├─ Call core.git_operations.push()
   ├─ Handle errors
   └─ Render output via ui/
   ↓
4. User sees result
```

### AI Command Flow

```
1. User: run-git commit-ai
   ↓
2. commands/commit_ai.py
   ├─ Get git diff (core/git_operations)
   ├─ Clean diff (utils/diff_cleaner)
   └─ Send to ai/client.py
   ↓
3. ai/client.py
   ├─ Get provider (ai/factory.py)
   ├─ Format prompt (ai/prompts/commit_prompt.py)
   ├─ Call provider API
   └─ Parse response
   ↓
4. Return formatted commit message
```

---

## Configuration

**Location**: `~/.config/run-git/config.yaml` (user-level)

**Settings**:
```yaml
ai:
  provider: openai
  model: gpt-4o
  api_key: ${OPENAI_API_KEY}

github:
  token: ${GITHUB_TOKEN}

defaults:
  branch: main
  remote: origin
```

---

## Error Handling

**Custom exceptions** in `exceptions.py`:
- `GitPushError` - Base exception
- `NotARepositoryError` - Not a git repo
- `NoChangesError` - No staged changes
- `MergeConflictError` - Merge conflicts exist
- `InvalidConfigError` - Configuration error

**Pattern**:
```python
try:
    result = core.operation()
except GitPushError as e:
    ui.show_error(str(e))
    raise SystemExit(1)
```

---

## Testing Strategy

**Framework**: pytest

**Structure**:
- `tests/test_basic.py` - Core functionality
- Use temporary directories for repo operations
- Mock external APIs where needed

**Run tests**:
```bash
pytest tests/
```

---

## Extension Points

### Adding a new command

1. Create `commands/new_command.py`
2. Define Click command
3. Implement in `cli.py`:
   ```python
   from gitpush.commands import new_command
   cli.add_command(new_command.new_command)
   ```

### Adding AI provider

1. Create `ai/providers/my_provider.py`
2. Implement base provider interface
3. Register in `ai/factory.py`

---

## Related Files

- `SPEC.md` - Product specification
- `PROJECT_OVERVIEW.md` - Project overview
- `cli.py` - CLI entry point
- `core/git_operations.py` - Git operations
- `ai/client.py` - AI client
