"""
Core Git operations for gitpush
"""

from __future__ import annotations
import os
import re
from typing import Optional, Dict, List, Any
import git
from git.exc import GitCommandError, InvalidGitRepositoryError
from gitpush.ui.banner import show_success, show_error, show_warning, show_info, show_progress

# Constants
VALID_BRANCH_PATTERN = re.compile(r"^[a-zA-Z0-9._\-/]+$")
MAX_BRANCH_NAME_LENGTH = 100


class GitOperations:
    """Handle all git operations"""

    def __init__(self, path: str = "."):
        self.path = path
        self.repo: Optional[git.Repo] = None
        self._initialize_repo()

    @staticmethod
    def validate_branch_name(branch_name: str) -> bool:
        """Validate branch name to prevent command injection"""
        if not branch_name or len(branch_name) > MAX_BRANCH_NAME_LENGTH:
            return False
        return bool(VALID_BRANCH_PATTERN.match(branch_name))

    def _initialize_repo(self):
        """Initialize git repository"""
        try:
            self.repo = git.Repo(self.path)
        except InvalidGitRepositoryError:
            self.repo = None

    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        return self.repo is not None

    def init_repo(self, remote_url: Optional[str] = None) -> bool:
        """Initialize a new git repository"""
        try:
            if self.is_git_repo():
                show_warning("Already a git repository")
                return True

            show_progress("Initializing git repository...")
            self.repo = git.Repo.init(self.path)
            show_success("Git repository initialized")

            if remote_url:
                self.add_remote("origin", remote_url)

            return True
        except Exception as e:
            show_error(f"Failed to initialize repository: {str(e)}")
            return False

    def add_remote(self, name, url):
        """Add a remote repository"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository. Run 'gitpush init' first")
                return False

            # Check if remote already exists
            if name in [remote.name for remote in self.repo.remotes]:
                show_warning(f"Remote '{name}' already exists. Updating URL...")
                self.repo.delete_remote(name)

            show_progress(f"Adding remote '{name}'...")
            self.repo.create_remote(name, url)
            show_success(f"Remote '{name}' added successfully")
            return True
        except Exception as e:
            show_error(f"Failed to add remote: {str(e)}")
            return False

    def get_status(self):
        """Get repository status"""
        if not self.is_git_repo():
            return None

        try:
            try:
                staged = [item.a_path for item in self.repo.index.diff("HEAD")]
            except git.BadName:
                staged = []

            untracked = list(self.repo.untracked_files)
            modified = [item.a_path for item in self.repo.index.diff(None)]
            status = {
                "untracked": untracked,
                "modified": modified,
                "staged": staged,
                "branch": self.repo.active_branch.name,
                "has_changes": len(untracked) > 0 or len(modified) > 0,
            }
            return status
        except Exception as e:
            show_error(f"Failed to get status: {str(e)}")
            return None

    def add_all(self):
        """Add all changes to staging"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            show_progress("Adding all changes to staging...")
            self.repo.git.add(A=True)
            show_success("All changes added to staging")
            return True
        except Exception as e:
            show_error(f"Failed to add changes: {str(e)}")
            return False

    def commit(self, message):
        """Commit changes"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            show_progress(f"Committing changes...")
            self.repo.index.commit(message)
            show_success(f"Changes committed: {message}")
            return True
        except Exception as e:
            show_error(f"Failed to commit: {str(e)}")
            return False

    def pull(self, remote="origin", branch=None):
        """Pull changes from remote"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            if branch is None:
                branch = self.repo.active_branch.name

            show_progress(f"Pulling from {remote}/{branch}...")
            self.repo.git.pull(remote, branch)
            show_success(f"Successfully pulled from {remote}/{branch}")
            return True
        except GitCommandError as e:
            if "CONFLICT" in str(e):
                show_error("Merge conflict detected! Please resolve conflicts manually.")
                return False
            else:
                show_error(f"Failed to pull: {str(e)}")
                return False
        except Exception as e:
            show_error(f"Failed to pull: {str(e)}")
            return False

    def push(self, remote="origin", branch=None, force=False):
        """Push changes to remote"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            if branch is None:
                branch = self.repo.active_branch.name

            show_progress(f"Pushing to {remote}/{branch}...")

            if force:
                self.repo.git.push(remote, branch, force=True)
            else:
                self.repo.git.push(remote, branch)

            show_success(f"Successfully pushed to {remote}/{branch}")
            return True
        except GitCommandError as e:
            if "rejected" in str(e):
                show_error("Push rejected. Try pulling first or use --force (dangerous!)")
                return False
            else:
                show_error(f"Failed to push: {str(e)}")
                return False
        except Exception as e:
            show_error(f"Failed to push: {str(e)}")
            return False

    def get_branches(self):
        """Get list of branches"""
        try:
            if not self.is_git_repo():
                return []

            branches = [branch.name for branch in self.repo.branches]
            return branches
        except Exception as e:
            show_error(f"Failed to get branches: {str(e)}")
            return []

    def create_branch(self, branch_name):
        """Create a new branch"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            # Validate branch name
            if not self.validate_branch_name(branch_name):
                show_error(f"Invalid branch name: '{branch_name}'")
                return False

            show_progress(f"Creating branch '{branch_name}'...")
            self.repo.create_head(branch_name)
            show_success(f"Branch '{branch_name}' created")
            return True
        except Exception as e:
            show_error(f"Failed to create branch: {str(e)}")
            return False

    def switch_branch(self, branch_name):
        """Switch to a branch"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            # Validate branch name
            if not self.validate_branch_name(branch_name):
                show_error(f"Invalid branch name: '{branch_name}'")
                return False

            show_progress(f"Switching to branch '{branch_name}'...")
            self.repo.git.checkout(branch_name)
            show_success(f"Switched to branch '{branch_name}'")
            return True
        except Exception as e:
            show_error(f"Failed to switch branch: {str(e)}")
            return False

    def delete_branch(self, branch_name, force=False):
        """Delete a branch"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            # Validate branch name
            if not self.validate_branch_name(branch_name):
                show_error(f"Invalid branch name: '{branch_name}'")
                return False

            current_branch = self.repo.active_branch.name
            if branch_name == current_branch:
                show_error(f"Cannot delete current branch '{branch_name}'")
                return False

            show_progress(f"Deleting branch '{branch_name}'...")
            if force:
                self.repo.delete_head(branch_name, force=True)
            else:
                self.repo.delete_head(branch_name)
            show_success(f"Branch '{branch_name}' deleted")
            return True
        except Exception as e:
            show_error(f"Failed to delete branch: {str(e)}")
            return False

    def get_log(self, max_count=10):
        """Get commit log"""
        try:
            if not self.is_git_repo():
                return []

            commits = []
            for commit in self.repo.iter_commits(max_count=max_count):
                commits.append(
                    {
                        "hash": commit.hexsha[:7],
                        "author": commit.author.name,
                        "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M"),
                        "message": commit.message.strip(),
                    }
                )
            return commits
        except Exception as e:
            show_error(f"Failed to get log: {str(e)}")
            return []

    def get_staged_diff(self) -> str:
        """Get staged diff (`git diff --staged`)."""
        if not self.is_git_repo() or self.repo is None:
            return ""

        try:
            return self.repo.git.diff("--staged")
        except Exception as e:
            show_error(f"Failed to read staged diff: {str(e)}")
            return ""

    def get_working_diff(self) -> str:
        """Get unstaged working-tree diff (`git diff`)."""
        if not self.is_git_repo() or self.repo is None:
            return ""

        try:
            return self.repo.git.diff()
        except Exception as e:
            show_error(f"Failed to read working diff: {str(e)}")
            return ""

    def get_branch_diff(self, base_branch: str = "main", head_ref: str = "HEAD") -> str:
        """Get full diff between branches using three-dot comparison."""
        if not self.is_git_repo() or self.repo is None:
            return ""

        resolved_base = self._resolve_branch_reference(base_branch)
        if not resolved_base:
            show_error(f"Base branch '{base_branch}' not found")
            return ""

        try:
            return self.repo.git.diff(f"{resolved_base}...{head_ref}")
        except Exception as e:
            show_error(f"Failed to read branch diff: {str(e)}")
            return ""

    def get_recent_commit_messages(self, limit: int = 5, rev: str = "HEAD") -> List[str]:
        """Get recent commit subjects from a revision."""
        if not self.is_git_repo() or self.repo is None:
            return []

        try:
            messages: List[str] = []
            for commit in self.repo.iter_commits(rev=rev, max_count=limit):
                messages.append(commit.message.strip().split("\n")[0])
            return messages
        except Exception as e:
            show_error(f"Failed to read commit messages: {str(e)}")
            return []

    def _resolve_branch_reference(self, branch_name: str) -> Optional[str]:
        """Resolve branch name to local or origin/<branch> reference."""
        if not self.is_git_repo() or self.repo is None:
            return None

        candidates = [branch_name, f"origin/{branch_name}"]
        for candidate in candidates:
            try:
                self.repo.commit(candidate)
                return candidate
            except Exception:
                continue

        return None

    def check_sensitive_files(self):
        """Check for sensitive files before commit"""
        sensitive_patterns = [
            ".env",
            ".env.local",
            ".env.production",
            "secrets.json",
            "credentials.json",
            "id_rsa",
            "id_dsa",
            ".pem",
            "password",
            "secret",
            "token",
        ]

        status = self.get_status()
        if not status:
            return []

        all_files = status["untracked"] + status["modified"]
        sensitive_files = []

        for file in all_files:
            for pattern in sensitive_patterns:
                if pattern.lower() in file.lower():
                    sensitive_files.append(file)
                    break

        return sensitive_files

    # ============================================================
    # TAG OPERATIONS
    # ============================================================

    def list_tags(self) -> List[Dict[str, Any]]:
        """List all local tags with their details."""
        try:
            if not self.is_git_repo():
                return []

            tags = []
            for tag in self.repo.tags:
                tag_info = {
                    "name": tag.name,
                    "commit": tag.commit.hexsha[:7] if hasattr(tag, "commit") else "N/A",
                    "message": tag.tag.message if hasattr(tag, "tag") and tag.tag else "",
                    "date": (
                        tag.tag.taggerdate.strftime("%Y-%m-%d %H:%M")
                        if hasattr(tag, "tag") and tag.tag and hasattr(tag.tag, "taggerdate")
                        else ""
                    ),
                }
                tags.append(tag_info)
            return tags
        except Exception as e:
            show_error(f"Failed to list tags: {str(e)}")
            return []

    def create_tag(
        self, tag_name: str, message: Optional[str] = None, annotated: bool = True
    ) -> bool:
        """Create a new tag (annotated or lightweight)."""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            # Validate tag name
            if not self._is_valid_tag_name(tag_name):
                show_error(
                    f"Invalid tag name: '{tag_name}'. "
                    "Use letters, numbers, dots, hyphens, underscores, and start with letter/number."
                )
                return False

            # Check if tag already exists
            if self.tag_exists(tag_name):
                show_warning(f"Tag '{tag_name}' already exists")
                return False

            show_progress(f"Creating tag '{tag_name}'...")

            if annotated:
                # Create annotated tag
                if not message:
                    message = f"Release {tag_name}"
                self.repo.create_tag(tag_name, message=message)
            else:
                # Create lightweight tag
                self.repo.create_tag(tag_name)

            show_success(f"Tag '{tag_name}' created successfully")
            return True

        except Exception as e:
            show_error(f"Failed to create tag: {str(e)}")
            return False

    def tag_exists(self, tag_name: str) -> bool:
        """Check if a tag exists locally."""
        try:
            if not self.is_git_repo():
                return False
            return tag_name in [tag.name for tag in self.repo.tags]
        except Exception:
            return False

    def delete_tag(self, tag_name: str) -> bool:
        """Delete a local tag."""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            if not self.tag_exists(tag_name):
                show_error(f"Tag '{tag_name}' does not exist")
                return False

            show_progress(f"Deleting tag '{tag_name}'...")
            self.repo.delete_tag(tag_name)
            show_success(f"Tag '{tag_name}' deleted")
            return True

        except Exception as e:
            show_error(f"Failed to delete tag: {str(e)}")
            return False

    def push_tag(self, tag_name: str, remote: str = "origin") -> bool:
        """Push a tag to remote."""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            if not self.tag_exists(tag_name):
                show_error(f"Tag '{tag_name}' does not exist")
                return False

            show_progress(f"Pushing tag '{tag_name}' to {remote}...")
            self.repo.git.push(remote, tag_name)
            show_success(f"Tag '{tag_name}' pushed to {remote}")
            return True

        except GitCommandError as e:
            show_error(f"Failed to push tag: {str(e)}")
            return False
        except Exception as e:
            show_error(f"Failed to push tag: {str(e)}")
            return False

    def push_all_tags(self, remote: str = "origin") -> bool:
        """Push all tags to remote."""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False

            tags = self.list_tags()
            if not tags:
                show_warning("No tags to push")
                return False

            show_progress(f"Pushing all tags to {remote}...")
            self.repo.git.push(remote, "--tags")
            show_success(f"All tags pushed to {remote}")
            return True

        except GitCommandError as e:
            show_error(f"Failed to push tags: {str(e)}")
            return False
        except Exception as e:
            show_error(f"Failed to push tags: {str(e)}")
            return False

    def get_remote_url(self) -> Optional[str]:
        """Get the remote origin URL."""
        try:
            if not self.is_git_repo():
                return None
            if self.repo.remotes:
                return self.repo.remotes.origin.url
            return None
        except Exception:
            return None

    @staticmethod
    def _is_valid_tag_name(tag_name: str) -> bool:
        """Validate tag name format."""
        if not tag_name or len(tag_name) > 100:
            return False
        # Tag name can contain letters, numbers, dots, hyphens, underscores
        # and must not start with special characters
        pattern = r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$"
        return bool(re.match(pattern, tag_name))
