# Changelog

All notable changes to this project will be documented in this file.

[1.0.9] - 2026-03-18

### 🛠 Fixes

* 🧩 Fixed GitHubManager missing method issue (`get_license_templates`)
* ❌ Removed GitHub-side file creation (gitignore/license templates)
* 🔥 Eliminated hidden commits causing push failures
* ⚠️ Fixed commit crash when no staged files exist
* 🔁 Improved push retry logic stability

---

### ⚡ Improvements

* 🧠 Fully shifted to **local-first repository setup**
* 🔗 Clean remote origin configuration (no token injection hacks)
* 🚀 Stable push using explicit refspec (`main:main`)
* 🧹 Better branch handling (safe rename to main)
* 📦 Cleaner CLI flow and error handling

---

### 🔐 Security & API

* 🔐 Improved GitHub token handling
* 🛡 Switched to Bearer token for API requests
* 📡 Better API error visibility (gitignore/license fetch)

---

### 🎯 Result

* ✅ No push conflicts
* ✅ No hidden commits
* ✅ Clean Git workflow
* ✅ Reliable repo creation every time

---


[1.0.8] - 2026-03-18

### ✨ Major Fixes

* 🔥 Fixed "failed to push some refs" error
* ✅ Ensured GitHub repositories are created EMPTY (`auto_init=False`)
* ❌ Removed gitignore & license creation on GitHub (now handled locally)
* 🔁 Added robust push retry mechanism (pull + push fallback)
* 🔗 Fixed remote origin handling and cleanup

---

### 🛠 Improvements

* ⚡ Clean GitPython push using explicit refspec (`main:main`)
* 🧠 Smart commit handling (avoids empty commit crashes)
* 🔐 Improved authentication flow (secure token handling)
* 📦 Better error handling and CLI feedback
* 🧹 Cleaner repository initialization flow

---

### 🧠 Internal Enhancements

* Improved GitHub API usage (Bearer token support)
* Removed unstable token-based push URL hack
* Better branch handling (safe rename to main)
* More reliable staging and commit detection

---

### 🎯 Result

* 🚀 100% reliable repo creation + push
* 🧩 No merge conflicts on first push
* ⚙️ Production-ready Git automation

---


[1.0.7] - 2026-03-18
🆕 Added

Smart Folder Detection: Automatically detects and lists existing files in folder before creating repository

Shows all files in current directory
Asks for confirmation before including them
Prevents accidental overwrites


Existing Repository Handling: Intelligent handling of existing git repositories

Detects if folder is already a git repository
Option to connect existing local repo to new GitHub repository
Smart remote management (replace or keep existing)


File Conflict Prevention: Never overwrites existing files

Skips .gitignore if already exists
Skips LICENSE if already exists
Skips README.md if already exists
Clear messages for each skipped file


Enhanced Remote Management:

Detects existing remote 'origin'
Option to replace or keep existing remote
Safe remote URL updates



🔧 Improved

URL Handling: Fixed "protocol 'https' is not supported" error

Removes all whitespace and invisible characters from URLs
Clean URL formatting before remote operations
Robust URL validation


Authentication: Token-based push authentication

Embeds GitHub token in push URL
More reliable authentication on Windows
Better credential handling


Push Reliability: Enhanced push mechanism

Uses set_upstream=True flag
Force push option on conflicts
Better sync with remote repositories


Commit Messages: Context-aware commit messages

"Initial commit" for new repositories
"Connect to GitHub repository" for existing repos
Clearer commit descriptions


User Feedback: More informative progress messages

Shows what files are being staged
Clear indication of skipped operations
Better success/warning/error messages



🐛 Fixed

Critical: Fixed push failures due to malformed URLs
Fixed "protocol 'https' is not supported" error
Fixed issues with existing git repositories
Fixed remote 'origin' conflicts
Improved handling of unrelated histories
Better error recovery on push failures

🎯 User Experience

Confirmation Prompts: Ask before important operations

Confirm before including existing files
Confirm before replacing remotes
Confirm before connecting existing repos


Smart Defaults: Intelligent behavior based on context

Auto-detects if folder has files
Preserves existing git history
Handles all edge cases gracefully

## [1.0.6] - 2026-03-15
 
### 🆕 Added
- **Interactive Menu Integration**: "Create New Repo" option now available in interactive mode
  - Access via `run-git` → Select "🆕 Create New Repo"
  - Full interactive workflow with guided prompts
  - Same powerful features as CLI command
 
### 🔧 Improved
- **Enhanced Push Reliability**: Improved repository push mechanism with automatic retry
  - Smart branch management (ensures `main` branch)
  - Automatic sync with remote on conflicts
  - Graceful error handling with manual fallback options
- **Better Git Add**: Using `git.add(A=True)` for more reliable file staging
- **Branch Naming**: Automatically uses `main` branch (not `master`)
- **Conflict Resolution**: Auto-handles unrelated histories with `--allow-unrelated-histories`
 
### 🐛 Fixed
- Fixed push failures when remote has diverged
- Improved error messages for failed operations
- Better handling of repository state conflicts
- Fixed branch naming inconsistencies
 
### 📚 Documentation
- Updated README with interactive mode usage
- Enhanced troubleshooting section
- Added error handling examples

---
## 📦 RUN-GIT v1.0.5 – 2026-03-13

### ✨ Improvements

* Improved **Git push reliability** during repository creation.
* Ensured default branch is automatically set to **main**.
* Replaced `git add *` with `git add -A` for better file tracking.
* Improved repository initialization workflow.

### 🐛 Bug Fixes

* Fixed **"refusing to merge unrelated histories"** error during first push.
* Fixed push failures when GitHub repository already contained commits.
* Improved handling of repositories with existing remote configuration.

### 🔧 Internal Changes

* Added retry logic for push operations.
* Automatic **pull + sync** if initial push fails.
* Improved CLI stability and error messages.

### 🚀 Example

```bash
run-git new my-project --quick
```

Creates a GitHub repository and pushes it instantly.

### 📦 Installation

```bash
pip install --upgrade run-git
```

### 🔗 Repository

https://github.com/himanshu231204/gitpush

---

⭐ If you find this project useful, consider giving it a star.


## [1.0.4] - 2026-03-13
 
### 🆕 Added
- **GitHub Repository Creation**: New `run-git new` command to create GitHub repositories directly from terminal
  - Smart language detection (Python, Node, Java, Go, Rust, and 160+ more)
  - Auto-generates .gitignore files for detected languages
  - License support (MIT, Apache 2.0, GPL v3, BSD, ISC)
  - Professional README template generation
  - One-time GitHub token setup with secure storage
  - Quick mode (`--quick`) for instant repo creation with smart defaults
  - Interactive mode for full customization
- Secure token storage in `~/.run-git/config.yml` with user-only permissions
- Automatic repo name conflict detection with suggestions
- Support for public and private repositories
 
### 🔧 Improved
- Enhanced error handling for network issues
- Better user feedback with progress indicators
- Cross-platform token storage support (Windows/Mac/Linux)
- Improved documentation with detailed setup guides
 
### 🐛 Fixed
- Token validation improvements
- Better handling of existing repositories
- Enhanced cross-platform compatibility
## [1.0.0] - 2026

### Added
- 🎉 Initial release of gitpush
- ⚡ Quick push command
- 🤖 Intelligent commit messages
- 🔀 Interactive conflict resolution
- 🌿 Branch management
- 📊 Beautiful terminal UI
- 🔐 Sensitive file detection

Created by: Himanshu Kumar (@himanshu231204)
