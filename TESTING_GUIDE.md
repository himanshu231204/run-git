<!-- Context: documentation/testing-guide | Priority: high | Version: 1.0 | Updated: 2026-04-05 -->

# RUN-GIT Testing Guide

> Comprehensive testing guide for RUN-GIT.

## Quick Reference

- **Purpose**: Understand testing procedures and run tests
- **Update When**: Adding tests or fixing bugs
- **Audience**: Developers, QA

---

## Running Tests

### Full Test Suite

```bash
pytest tests/
```

### With Coverage

```bash
pytest tests/ -v --cov=gitpush --cov-report=term
```

---

## Test Structure

```
tests/
├── __init__.py
└── test_basic.py         # Main test file
```

### Test Classes

| Class | Tests |
|-------|-------|
| `TestGitOperations` | Git add, commit, push, pull |
| `TestBranchOperations` | Branch create, switch, merge |
| `TestStatusCommands` | Status, log, graph |
| `TestAICommands` | AI commit, PR, review |

---

## Single Tests

### Run Specific Test

```bash
pytest tests/test_basic.py::TestGitOperations::test_commit -v
```

### Run Test Class

```bash
pytest tests/test_basic.py::TestGitOperations -v
```

### Run by Name

```bash
pytest tests/test_basic.py -k commit -v
```

---

## Using unittest

```bash
python -m unittest tests.test_basic.TestGitOperations.test_commit
python -m unittest tests.test_basic.TestGitOperations -v
```

---

## Test Patterns

### AAA Pattern

```python
def test_example(self):
    # Arrange
    setup_data = self.create_fixtures()

    # Act
    result = function_under_test(setup_data)

    # Assert
    self.assertEqual(result, expected)
```

### Using Temp Directories

```python
import tempfile
import shutil

class TestGitOperations(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
```

---

## Writing Tests

### Basic Test

```python
import unittest
from gitpush.core.git_operations import GitOperations


class TestGitOperations(unittest.TestCase):
    def test_add(self):
        git = GitOperations()
        result = git.add(".")
        self.assertTrue(result)
```

### Mocking External APIs

```python
from unittest.mock import patch, MagicMock


class TestAICommands(unittest.TestCase):
    @patch("gitpush.ai.client.OpenAI")
    def test_commit_ai(self, mock_openai):
        mock_openai.return_value.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="feat: test"))]
        )
        # Test code
```

---

## CI Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -e ".[test]"
      - name: Run tests
        run: pytest tests/
```

---

## Coverage

### Generate Report

```bash
pytest tests/ --cov=gitpush --cov-report=html
```

### View HTML Report

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## Common Issues

### Import Errors

```bash
# Reinstall package
pip install -e .
```

### Test Discovery

```bash
pytest tests/ --collect-only
```

### Cleanup

```bash
# Remove cache
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov
```

---

## Related Files

- `test_basic.py` - Main test file
- `pyproject.toml` - Test configuration
- `DEVELOPMENT_GUIDE.md` - Development guide
