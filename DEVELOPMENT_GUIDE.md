<!-- Context: documentation/development-guide | Priority: high | Version: 1.0 | Updated: 2026-04-05 -->

# RUN-GIT Development Guide

> Comprehensive guide for developers contributing to RUN-GIT.

## Quick Reference

- **Purpose**: Set up development environment and understand codebase
- **Update When**: Adding features, fixing bugs, or contributing
- **Audience**: Developers, contributors

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Code editor (VS Code recommended)

---

### Setup

```bash
# Clone repository
git clone https://github.com/himanshu231204/run-git.git
cd run-git

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -e ".[test]"

# Install dev tools
pip install black flake8 pylint build twine
```

---

## Running Commands

### Test Commands

```bash
pytest tests/
pytest tests/ -v --cov=gitpush --cov-report=term
```

### Single Tests

```bash
pytest tests/test_basic.py::TestGitOperations::test_commit -v
pytest tests/test_basic.py::TestGitOperations -v
pytest tests/test_basic.py -k commit -v
python -m unittest tests.test_basic.TestGitOperations.test_commit
```

---

## Code Style

### Formatting (Black)

```bash
black gitpush tests
black --check gitpush/
```

### Linting (Flake8)

```bash
flake8 gitpush/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 gitpush/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

### Type Checking (Pylint)

```bash
pylint gitpush/
```

---

## Building

### Build Package

```bash
python -m build
twine check dist/*
```

### Install Locally

```bash
pip install -e .
```

---

## Project Structure

```
gitpush/
├── cli.py                 # Main CLI entry (Click)
├── commands/              # Command handlers (thin)
│   ├── push.py
│   ├── branch.py
│   ├── commit_ai.py
│   └── ...
├── core/                 # Business logic
│   ├── git_operations.py
│   ├── commit_generator.py
│   └── ...
├── ai/                   # AI integration
│   ├── client.py
│   ├── factory.py
│   ├── prompts/
│   └── providers/
├── ui/                   # Terminal UI (Rich)
├── utils/                # Utilities
├── config/               # Configuration
└── exceptions.py         # Custom exceptions
```

---

## Adding Commands

### 1. Create Command File

Create `gitpush/commands/new_command.py`:

```python
import click
from gitpush.ui.banner import show_success


@click.command()
@click.option("--option", "-o", help="Option description")
@click.pass_context
def new_command(ctx, option):
    """Short description of command."""
    click.echo(f"Running with option: {option}")
    show_success("Done!")
```

### 2. Register in CLI

Edit `cli.py`:

```python
from gitpush.commands import new_command

cli.add_command(new_command.new_command)
```

---

## Adding AI Providers

### 1. Create Provider

Create `gitpush/ai/providers/my_provider.py`:

```python
from gitpush.ai.providers.base import BaseProvider


class MyProvider(BaseProvider):
    name = "my_provider"

    def generate(self, prompt, **kwargs):
        # Implement API call
        return "generated response"
```

### 2. Register Provider

Edit `gitpush/ai/factory.py`:

```python
from gitpush.ai.providers.my_provider import MyProvider

PROVIDERS = {
    "my_provider": MyProvider,
    # ...
}
```

---

## Code Standards

### Imports

```python
# Group: stdlib, third-party, local
import os
import click

from gitpush.core import git_operations
from gitpush.ui.banner import show_success
```

### Naming

- Files: `snake_case.py`
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### Type Hints

```python
def function(arg: str) -> int:
    return len(arg)
```

---

## Testing

### Write Tests

```python
import unittest
from gitpush.core.git_operations import GitOperations


class TestGitOperations(unittest.TestCase):
    def setUp(self):
        # Setup test repo
        pass

    def test_commit(self):
        # Test code
        pass
```

### Run Specific Tests

```bash
pytest tests/test_basic.py -k "test_name" -v
```

---

## Common Tasks

### Add Dependency

1. Edit `pyproject.toml`:
   ```toml
   dependencies = [
       "new_package>=1.0.0",
   ]
   ```

2. Rebuild:
   ```bash
   pip install -e .
   ```

### Update Version

Edit `pyproject.toml`:
```toml
version = "1.4.0"  # Increment as needed
```

---

## CI Checks

Run locally before submitting:

```bash
black --check gitpush/
flake8 gitpush/ --count --select=E9,F63,F7,F82 --show-source --statistics
pytest tests/
python -m build
twine check dist/*
```

---

## Documentation

### Update README

- Keep features table current
- Update command reference
- Verify examples work

### Add Context Files

For new features, add context files in `.opencode/context/`:

```
.opencode/context/development/
├── features/
│   └── new-feature.md
```

---

## Troubleshooting

### Import Errors

```bash
# Reinstall package
pip install -e .
```

### Test Failures

```bash
# Clean and reinstall
pip uninstall run-git
pip install -e ".[test]"
```

### Lint Errors

```bash
# Auto-fix with black
black gitpush/
```

---

## Related Files

- `AGENTS.md` - Agent instructions
- `ARCHITECTURE.md` - Technical architecture
- `API_REFERENCE.md` - Command reference
- `pyproject.toml` - Project configuration
