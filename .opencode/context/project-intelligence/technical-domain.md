<!-- Context: project-intelligence/technical | Priority: critical | Version: 1.1 | Updated: 2026-04-05 -->

# Technical Domain

> Document the technical foundation, architecture, and key decisions.

## Quick Reference

- **Purpose**: Understand how RUN-GIT works technically
- **Update When**: New features, refactoring, tech stack changes
- **Audience**: Developers, contributors, AI agents

---

## Primary Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Language | Python | 3.8+ | Cross-platform, rich ecosystem |
| CLI Framework | Click | 8.0+ | Simple, extensible command handling |
| UI Library | Rich | 13.0+ | Beautiful terminal output |
| Git Integration | GitPython | 3.1+ | Pure Python git operations |
| Interactive Prompts | Questionary | 1.10+ | User-friendly prompts |
| HTTP Requests | Requests | 2.28+ | API calls |
| YAML Config | PyYAML | 6.0+ | Configuration management |
| GitHub API | PyGithub | 1.59+ | GitHub integration |

---

## Architecture Pattern

```
Type: CLI Tool (Monolith)
Pattern: Layered architecture with separation of concerns

CLI Layer (cli.py) → Commands (commands/) → Core (core/) → Git/AI
```

### Why This Architecture?

- **Separation of concerns**: Commands are thin orchestrators, core contains business logic
- **Testability**: Core logic has no CLI dependencies, easy to unit test
- **Extensibility**: New commands added as isolated modules
- **AI Integration**: Dedicated AI layer with provider abstraction

---

## Project Structure

```
gitpush/
├── cli.py                    # Main CLI entry (Click)
├── commands/                 # Command handlers (thin orchestration)
│   ├── push.py              # Push workflow
│   ├── branch.py            # Branch operations
│   ├── commit_ai.py          # AI commit messages
│   ├── pr_ai.py             # AI PR descriptions
│   ├── review_ai.py         # AI code review
│   └── ...
├── core/                     # Business logic (testable)
│   ├── git_operations.py    # Git operations wrapper
│   ├── commit_generator.py  # Auto message generation
│   ├── conflict_resolver.py # Merge conflict handling
│   ├── graph_renderer.py    # ASCII graph rendering
│   └── ai_engine.py        # AI orchestration
├── ai/                       # AI integration layer
│   ├── client.py            # Unified AI client
│   ├── factory.py           # Provider selector
│   ├── config.py            # AI configuration
│   ├── prompts/             # Prompt templates
│   │   ├── commit_prompt.py
│   │   ├── pr_prompt.py
│   │   └── review_prompt.py
│   └── providers/           # AI provider implementations
│       ├── openai.py       # OpenAI GPT
│       ├── anthropic.py    # Anthropic Claude
│       ├── grok.py         # xAI Grok
│       ├── google.py       # Google Gemini
│       └── local.py       # Local Ollama/LM Studio
├── ui/                       # Terminal UI (Rich)
│   ├── banner.py           # ASCII banners
│   └── interactive.py       # Interactive menus
├── utils/                    # Utilities
│   ├── validators.py       # Input validation
│   ├── formatters.py       # Output formatting
│   ├── diff_cleaner.py     # Git diff cleaning
│   └── license.py          # License display
├── config/                   # Configuration
│   └── settings.py         # Settings management
└── exceptions.py            # Custom exceptions
```

---

## Key Technical Decisions

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Click over argparse | Better command grouping, help generation | Cleaner CLI code |
| Rich for all output | Consistent terminal appearance | Beautiful UI |
| GitPython for git ops | Pure Python, no external deps | Cross-platform |
| AI provider abstraction | Support multiple AI backends | Flexibility |
| Thin commands | Easy to test, maintain | Code quality |
| YAML config | Human-readable, nested config | Easy configuration |

---

## Integration Points

| System | Purpose | Protocol | Direction |
|--------|---------|----------|-----------|
| Git | Version control | GitPython | Internal |
| GitHub | Repository creation, PRs | PyGithub | Outbound |
| OpenAI | AI generation | OpenAI API | Outbound |
| Anthropic | AI generation | Anthropic API | Outbound |
| xAI | AI generation | xAI API | Outbound |
| Google | AI generation | Google AI API | Outbound |
| Local AI | AI generation | HTTP (Ollama) | Local |

---

## Supported AI Providers

```python
# Example: Using different providers
run-git commit-ai --provider openai --model gpt-4o
run-git commit-ai --provider anthropic --model claude-3-5-sonnet
run-git commit-ai --provider grok --model grok-2
run-git commit-ai --provider google --model gemini-2.0-flash
run-git commit-ai --provider local --model llama3
```

---

## Code Patterns

### Command Pattern (Click)

```python
import click
from gitpush.ui.banner import show_success


@click.command()
@click.option("--message", "-m", help="Custom message")
@click.pass_context
def push(ctx, message):
    """Push changes to remote."""
    show_success("Changes pushed!")
```

### Core Pattern (Testable)

```python
def git_add(path: str) -> bool:
    """Add file to staging."""
    repo = get_current_repo()
    repo.index.add(path)
    return True
```

### AI Provider Pattern

```python
class OpenAIProvider:
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

---

## Development Environment

```
Setup: python -m venv .venv && pip install -e ".[test]"
Requirements: Python 3.8+, Git
Local Dev: python -m gitpush
Testing: pytest tests/
Formatting: black gitpush/
Linting: flake8 gitpush/
```

---

## Deployment

```
Environment: PyPI (pip install)
Platform: Cross-platform (Python)
CI/CD: GitHub Actions (tests.yml, quality.yml, publish.yml)
Monitoring: None (CLI tool)
```

---

## Onboarding Checklist

- [x] Know the primary tech stack (Python, Click, Rich, GitPython)
- [x] Understand the architecture pattern and why it was chosen
- [x] Know the key project directories and their purpose
- [x] Understand major technical decisions and rationale
- [x] Know integration points and dependencies
- [x] Be able to set up local development environment
- [x] Know how to run tests and deploy

---

## 📂 Codebase References

**Implementation**: `gitpush/cli.py` - Main CLI entry point
**Core Logic**: `gitpush/core/git_operations.py` - Git operations
**AI Engine**: `gitpush/ai/client.py` - AI client
**Config**: `pyproject.toml`, `gitpush/config/settings.py`

---

## Related Files

- `ARCHITECTURE.md` - Detailed architecture
- `API_REFERENCE.md` - CLI commands
- `DEVELOPMENT_GUIDE.md` - Development guide
- `pyproject.toml` - Project configuration
