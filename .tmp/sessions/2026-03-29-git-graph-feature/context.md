# Task Context: Git Visual Graph Tree Feature

Session ID: 2026-03-29-git-graph-feature
Created: 2026-03-29
Status: in_progress

## Current Request
Add a new `run-git graph` command that displays a visual commit tree with:
1. ASCII graph lines (like git log --graph)
2. File diff view in commit details

## Branch
feature/graph-visualization

## Reference Files
- `gitpush/cli.py` - Main CLI entry point
- `gitpush/commands/__init__.py` - Command exports
- `gitpush/commands/graph.py` - Graph command
- `gitpush/core/graph_renderer.py` - Graph building logic
- `gitpush/core/git_operations.py` - Git operations

## Project Tech Stack
- Click (CLI framework)
- GitPython (git operations)
- Rich (terminal UI)
- questionary (interactive prompts)

## Components to Update
1. `gitpush/core/graph_renderer.py` - Add ASCII graph line building
2. `gitpush/commands/graph.py` - Add file diff display in commit details

## Exit Criteria
- [x] ASCII graph lines show branch/merge structure
- [x] File diff view shows modified files with +/- counts
- [x] Command works properly
- [x] Pushed to branch feature/graph-visualization
