<!-- Context: project-intelligence/technical | Priority: high | Version: 1.2 | Updated: 2026-03-31 -->

# Technical Domain

> Document the technical foundation, architecture, and key decisions for the gitpush CLI tool.

## Quick Reference

- **Purpose**: Understand how the project works technically
- **Update When**: New features, refactoring, tech stack changes
- **Audience**: Developers, DevOps, technical stakeholders

## Primary Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Language | Python | 3.8+ | Cross-platform, widely available, good CLI support |
| Framework | Click | Latest | Mature, well-documented, easy to compose command groups |
| Database | None | N/A | CLI tool, no persistent data storage needed |
| Infrastructure | Local execution | N/A | Runs on developer machines |
| Key Libraries | rich, questionary, pytest, black, flake8 | Latest | Terminal UX, CLI interactivity, testing, code quality |

## Architecture Pattern

```
Type: Monolith (CLI tool)
Pattern: Modular command structure with separation of concerns
```

### Why This Architecture?

Simple CLI tool with clear separation: commands/ for CLI orchestration, core/ for business logic, ui/ for terminal rendering. Enables testable core logic without CLI dependencies.

## Project Structure

```
gitpush/
├── cli.py                  # Top-level Click command group
├── commands/               # Thin CLI orchestration layer
├── core/                   # Business logic (Git ops, commit generation, rendering)
├── ui/                     # Terminal UX (Rich, questionary)
├── utils/                  # Reusable helpers/validators
├── config/settings.py      # Config model + persistence
├── exceptions.py           # Domain exceptions
tests/                     # Automated tests
.github/workflows/         # CI (tests.yml, quality.yml, publish.yml)
```

**Key Directories**:
- `cli.py` - Entry point, Click command group definition
- `commands/` - Thin orchestration: parse args → call core → render output
- `core/` - Testable business logic without CLI dependencies
- `ui/` - Terminal rendering and user interaction (Rich, questionary)
- `utils/` - Reusable helpers and validators

## Key Technical Decisions

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Use Click for CLI framework | Mature, well-documented, easy to compose command groups | Clean command hierarchy, testable CLI logic |
| Separate concerns (commands/, core/, ui/) | CLI orchestration separate from business logic | Testable core without CLI dependencies |
| Type hints for public functions | Better IDE support, self-documenting code | Maintainable, clearer contracts |

## Integration Points

| System | Purpose | Protocol | Direction |
|--------|---------|----------|-----------|
| Git executable | Execute git commands (status, commit, push, etc.) | CLI subprocess | Outbound |
| Local filesystem | Read/write config files, repository files | OS file operations | Internal |

## Technical Constraints

| Constraint | Origin | Impact |
|------------|--------|--------|
| Windows compatibility | User requirement | Use PowerShell-compatible commands, cross-platform path handling |
| Python 3.8+ only | Language version constraint | Use only features available in Python 3.8+ |

## Development Environment

```
Setup: python -m venv .venv && .venv\Scripts\Activate.ps1 && pip install -e ".[test]"
Requirements: Python 3.8+, git executable
Local Dev: python -m gitpush or run-git (if installed)
Testing: pytest or python -m pytest tests/
```

## Deployment

```
Environment: PyPI package (distribution), local development
Platform: PyPI for package distribution, GitHub Actions for CI
CI/CD: GitHub Actions workflows (tests.yml, quality.yml, publish.yml)
Monitoring: None (CLI tool)
```

## Onboarding Checklist

- [ ] Know the primary tech stack (Python 3.8+, Click, rich, questionary)
- [ ] Understand the architecture pattern and why it was chosen
- [ ] Know the key project directories and their purpose
- [ ] Understand major technical decisions and rationale
- [ ] Know integration points and dependencies (Git executable, filesystem)
- [ ] Be able to set up local development environment
- [ ] Know how to run tests and deploy

## 📂 Codebase References

- **CLI Entry**: `gitpush/cli.py` - Top-level Click command group
- **Commands**: `gitpush/commands/` - Thin CLI orchestration layer
- **Core Logic**: `gitpush/core/` - Business logic (Git operations, commit generation)
- **UI Layer**: `gitpush/ui/` - Terminal UX (Rich, questionary)
- **Config**: `gitpush/config/settings.py` - Config model + persistence
- **Tests**: `tests/` - Automated tests (pytest, unittest style)

## Related Files

- `business-domain.md` - Why this technical foundation exists
- `business-tech-bridge.md` - How business needs map to technical solutions
- `decisions-log.md` - Full decision history with context

---

## Code Patterns

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Files | snake_case | `cli.py`, `git_operations.py` |
| Functions/Variables | snake_case | `get_status()`, `commit_message` |
| Classes | PascalCase | `GitOperations`, `CommitGenerator` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_BRANCH`, `MAX_MESSAGE_LENGTH` |
| Database | snake_case | N/A (no database) |

### Code Standards

1. **Formatting**: Follow Black formatting (line length 100 in pyproject.toml)
2. **Types**: Add type hints for public function signatures
3. **Imports**: Prefer absolute imports from `gitpush.*`, group: stdlib → third-party → local
4. **Architecture**: Keep `commands/` thin (parse args → call core → render output)
5. **Business Logic**: Keep reusable logic in `core/` (testable without CLI dependencies)
6. **UI Layer**: Keep terminal rendering and interaction in `ui/` (Rich, questionary)
7. **Validation**: Validate inputs early with `gitpush/utils/validators.py`
8. **Errors**: Use project exceptions from `gitpush/exceptions.py`
9. **Testing**: Follow AAA pattern (Arrange → Act → Assert)
10. **Constants**: Avoid hardcoded values, use config/settings

### Security Requirements

1. **No Secrets**: Never commit secrets or credentials to version control
2. **Input Sanitization**: Sanitize command arguments before passing to git subprocess
3. **Path Validation**: Validate file paths to prevent path traversal attacks
4. **Subprocess Safety**: Use subprocess with `shell=False` to prevent command injection
5. **Error Handling**: Handle errors gracefully without exposing sensitive information
6. **Config Security**: Don't store sensitive data in config files without encryption