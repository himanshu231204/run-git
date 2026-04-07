# Changelog

All notable changes to this project will be documented in this file.

[1.5.0] - 2026-04-08

### 🏷️ Tag & Release - New Feature

* **Interactive Tag Management Menu**:
  * Full menu-driven tag operations in TUI
  * View tags in professional Rich table format
  * Create, push, delete tags with confirmations

* **Tag Commands**:
  * `run-git tag <name>` - Create a new tag
  * `run-git tag <name> -m "message"` - Create with annotation
  * `run-git tag <name> --lightweight` - Create lightweight tag

* **Release Commands**:
  * `run-git tag <name> -r` - One-click: create tag + push + GitHub release
  * `run-git tag <name> -r --draft` - Create as draft release
  * `run-git tag <name> -r --ai` - Generate release notes with AI
  * `run-git release <name>` - Create release from existing tag

* **One-Click Release Flow**:
  * Create tag locally
  * Push tag to remote
  * Create GitHub release with title and notes
  * Support for manual or AI-generated release notes
  * Draft release option

* **GitHub Integration**:
  * New methods in GitHubManager: `create_release()`, `list_releases()`, `delete_release()`
  * New methods in GitOperations: `create_tag()`, `list_tags()`, `delete_tag()`, `push_tag()`, `push_all_tags()`
  * Repository name extraction from remote URL
  * Tag validation and error handling

* **UI Enhancements**:
  * Professional Rich panels and tables
  * Color-coded menu options
  * Confirmation prompts for destructive actions
  * Progress indicators during operations

### 🐛 Bug Fixes

* Fixed clone to non-empty directory - now offers temp directory option
* Added URL validation before cloning
* Improved error handling with specific messages
* URL cleaning - removes extra characters that could break URLs

[1.4.0] - 2026-03-30

### 🤖 AI Assistant - Major Update

* **Interactive AI Menu**:
  * Full menu-driven AI configuration
  * Provider selection (OpenAI, Anthropic, Google, Grok, Local)
  * API key input with masked password
  * Model selection from 50+ verified models

* **Code Review Features**:
  * **Full Review**: Review all changes in diff
  * **Single File Review**: Review specific files (NEW!)
  * **Detailed Analysis**: Bugs, Code Quality, Performance, Security, Best Practices
  * **Styled Output**: Rich markdown rendering in terminal

* **Provider Support** (50+ models):
  * OpenAI: gpt-4o, o1, o3-mini, o4-mini
  * Anthropic: claude-4-sonnet, claude-4-opus
  * Google: gemini-2.0-flash, gemini-2.5-pro
  * Grok: grok-2, grok-2-vision
  * Local: llama3.3, qwen2.5, deepseek-r1

* **Bug Fixes**:
  * Fixed Full Review with staged/working changes
  * Fixed missing imports in interactive mode
  * Fixed circular import issues
  * Consolidated imports at module top
  * Added settings migration for old configs
  * Improved error handling with helpful hints
  * Automatic model fallback on API errors

* **Code Quality**:
  * Externalized prompt templates
  * DRY principle in config defaults
  * Better error messages for users

### 🔐 PRO Feature Gating (from 1.3.0)

* **Tiered Access**:
  * FREE users: commit-ai (5/day), pr-ai (2/day), review-ai (3/day)
  * PRO users: Unlimited access to all features
* **Config Commands**:
  * `run-git config set-api-key <key>` - Store PRO API key
  * `run-git config status` - Show license status
  * `run-git config remove-api-key` - Remove API key (downgrade to FREE)
* **Upgrade Prompts**: Clear messages with option to open https://run-git.com
* **Usage Tracking**: Daily counters reset at midnight

### 🤖 Multi-Provider AI Support

* **Supported Providers**:
  * Local (Ollama) - default
  * OpenAI (GPT models)
  * Anthropic (Claude models)
  * Google (Gemini models) - NEW
  * Grok (xAI models) - NEW
* **Configuration**:
  * Environment variables (e.g., `RUN_GIT_AI_PROVIDER=google GOOGLE_API_KEY=key`)
  * Persistent config via `run-git config set ai_provider <provider>`
  * Per-command override with environment variables
* **Automatic Provider Selection**: Based on configuration with fallbacks

### 🌳 New Features - Commit Graph Visualization (from 1.2.0)

* **Graph Command** - New `run-git graph` command for visualizing commit history
* **ASCII Graph** - Branch visualization with lines using `--graph` flag
* **File Diff View** - See changed files with +/- counts using `--diff` flag
* **Interactive Mode** - Select commits to view details with `-i` flag
* **Specific Commit** - View any commit with `--commit <hash>`
* **Branch Tree** - Overview of all branches with `--tree` flag

### 🎨 UI Enhancements (from 1.2.0)

* **New Menu Option** - Commit Graph option in interactive menu
* **Updated Shortcuts** - Added 'g' keyboard shortcut for graph

### 📦 Other Improvements

* All 36 tests pass
* Backward compatible
* Windows-compatible Unicode handling
* Clean separation of concerns

[1.2.0] - 2026-03-29

### 🌳 New Features - Commit Graph Visualization

* **Graph Command** - New `run-git graph` command for visualizing commit history
* **ASCII Graph** - Branch visualization with lines using `--graph` flag
* **File Diff View** - See changed files with +/- counts using `--diff` flag
* **Interactive Mode** - Select commits to view details with `-i` flag
* **Specific Commit** - View any commit with `--commit <hash>`
* **Branch Tree** - Overview of all branches with `--tree` flag

### 🎨 UI Enhancements

* **New Menu Option** - Commit Graph option in interactive menu
* **Updated Shortcuts** - Added 'g' keyboard shortcut for graph

