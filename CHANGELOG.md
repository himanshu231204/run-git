# Changelog

All notable changes to this project will be documented in this file.

[1.2.0] - 2026-03-30

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

### 🔐 PRO Feature Gating System

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

### 📦 Other Improvements

* All 36 tests pass
* Backward compatible
* Windows-compatible Unicode handling
* Clean separation of concerns
