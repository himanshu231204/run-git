"""
GitHub integration for run-git
Production-ready version (no push conflicts)
"""

import os
import yaml
import logging
import requests
from pathlib import Path
from github import Github, GithubException
import questionary
from gitpush.ui.banner import show_success, show_error, show_warning, show_info, show_progress

# Configure logging
logger = logging.getLogger(__name__)


class GitHubManager:
    CONFIG_DIR = Path.home() / ".run-git"
    CONFIG_FILE = CONFIG_DIR / "config.yml"

    def __init__(self):
        self.token = None
        self.github = None
        self._load_config()

    # ============================================================
    # CONFIG
    # ============================================================
    def _load_config(self):
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, "r") as f:
                    config = yaml.safe_load(f)
                    self.token = config.get("github_token")
                    if self.token:
                        self.github = Github(self.token)
        except Exception as e:
            show_warning(f"Config load failed: {str(e)}")

    def _save_config(self):
        try:
            self.CONFIG_DIR.mkdir(exist_ok=True)

            with open(self.CONFIG_FILE, "w") as f:
                yaml.dump({"github_token": self.token}, f)

            os.chmod(self.CONFIG_FILE, 0o600)
            show_success("Token saved")

        except Exception as e:
            show_error(f"Save failed: {str(e)}")

    # ============================================================
    # AUTH
    # ============================================================
    def authenticate(self):
        if self.token and self.github:
            try:
                user = self.github.get_user()
                _ = user.login
                return True
            except Exception as e:
                logger.warning(f"Invalid saved token: {e}")
                self.token = None

        show_info("\nGitHub Token required")
        show_info("https://github.com/settings/tokens")
        show_info("Scopes: repo, user")

        token = questionary.password("Enter token:").ask()

        if not token:
            show_error("Token required")
            return False

        try:
            gh = Github(token)
            user = gh.get_user().login

            show_success(f"Logged in as {user}")

            self.token = token
            self.github = gh
            self._save_config()
            return True

        except Exception as e:
            show_error(f"Auth failed: {str(e)}")
            return False

    # ============================================================
    # HELPERS
    # ============================================================
    def get_gitignore_templates(self):
        return [
            "Python",
            "Node",
            "Java",
            "Go",
            "Rust",
            "C++",
            "C",
            "Ruby",
            "PHP",
            "Swift",
            "Kotlin",
            "Dart",
            "R",
        ]

    def get_license_templates(self):
        return {
            "MIT": "mit",
            "Apache 2.0": "apache-2.0",
            "GPL v3": "gpl-3.0",
            "BSD 3-Clause": "bsd-3-clause",
            "ISC": "isc",
            "None": None,
        }

    def repo_exists(self, name):
        try:
            self.github.get_user().get_repo(name)
            return True
        except Exception:
            return False

    def suggest_repo_name(self, base):
        i = 1
        while True:
            name = f"{base}-{i}"
            if not self.repo_exists(name):
                return name
            i += 1

    def detect_language(self):
        if Path("requirements.txt").exists():
            return "Python"
        elif Path("package.json").exists():
            return "Node"
        elif Path("pom.xml").exists():
            return "Java"
        return "Python"

    # ============================================================
    # CREATE REPOSITORY
    # ============================================================
    def create_repository(self, config):
        """
        Create EMPTY GitHub repository (NO FILES)

        Returns:
            Repo object or None on failure
        """
        # Validate repo name
        repo_name = config.get("name", "").strip()
        if not repo_name:
            show_error("Repository name cannot be empty")
            return None

        # Validate repo name format
        if not self._is_valid_repo_name(repo_name):
            show_error(
                "Invalid repository name. Use only letters, numbers, hyphens, and underscores."
            )
            return None

        try:
            user = self.github.get_user()

            # Check if repo already exists
            if self.repo_exists(repo_name):
                show_warning("Repository already exists")

                new_name = self.suggest_repo_name(repo_name)
                show_info(f"Suggested: {new_name}")

                if questionary.confirm(f"Use {new_name}?").ask():
                    config["name"] = new_name
                    repo_name = new_name
                else:
                    return None

            show_progress(f"Creating '{repo_name}'...")

            repo = user.create_repo(
                name=repo_name,
                description=config.get("description", ""),
                private=config.get("private", False),
                auto_init=False,
                has_issues=True,
                has_wiki=True,
                has_downloads=True,
            )

            # Validate the returned URLs
            clone_url = self._clean_url(getattr(repo, "clone_url", None))
            html_url = self._clean_url(getattr(repo, "html_url", None))

            if not clone_url or not html_url:
                show_error("Failed to get repository URLs")
                return None

            # Update repo attributes with cleaned URLs
            repo.clone_url = clone_url
            repo.html_url = html_url

            show_success(f"Created: {html_url}")
            return repo

        except GithubException as e:
            error_msg = e.data.get("message", str(e)) if hasattr(e, "data") else str(e)
            show_error(f"GitHub error: {error_msg}")
            return None

        except Exception as e:
            show_error(f"Failed to create repository: {str(e)}")
            return None

    def _is_valid_repo_name(self, name):
        """Validate repository name format."""
        import re

        # GitHub repo name rules: alphanumeric, hyphens, underscores, dots
        # Cannot start with hyphen or dot
        pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$|^[a-zA-Z0-9]$"
        return bool(re.match(pattern, name)) and len(name) <= 100

    def _clean_url(self, url):
        """Clean and validate URL."""
        if not url:
            return None

        # Strip whitespace and control characters
        url = url.strip()

        # Remove any ANSI codes or special characters
        import re

        url = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", url)

        # Validate it starts with http/https
        if not url.startswith(("http://", "https://")):
            return None

        return url

    # ============================================================
    # CONTENT FETCH
    # ============================================================
    def get_gitignore_content(self, template):
        try:
            url = f"https://api.github.com/gitignore/templates/{template}"
            headers = {"Authorization": f"Bearer {self.token}"}

            r = requests.get(url, headers=headers)

            if r.status_code == 200:
                return r.json().get("source", "")
            else:
                show_warning(f"Gitignore failed: {r.status_code}")
                return None

        except Exception as e:
            show_warning(str(e))
            return None

    def get_license_content(self, key, author):
        try:
            url = f"https://api.github.com/licenses/{key}"
            r = requests.get(url)

            if r.status_code == 200:
                text = r.json().get("body", "")

                import datetime

                year = str(datetime.datetime.now().year)

                text = text.replace("[year]", year)
                text = text.replace("[fullname]", author)

                return text
            else:
                show_warning(f"License failed: {r.status_code}")
                return None

        except Exception as e:
            show_warning(str(e))
            return None

    # ============================================================
    # TAG & RELEASE OPERATIONS
    # ============================================================

    def create_release(
        self,
        repo_name: str,
        tag_name: str,
        title: str,
        body: str = "",
        draft: bool = False,
        prerelease: bool = False,
    ):
        """
        Create a GitHub release.

        Args:
            repo_name: Name of the repository
            tag_name: Tag name to create release from
            title: Release title
            body: Release notes/description
            draft: Create as draft
            prerelease: Mark as prerelease

        Returns:
            Release object or None on failure
        """
        try:
            user = self.github.get_user()
            repo = user.get_repo(repo_name)

            show_progress(f"Creating release '{tag_name}'...")

            release = repo.create_release(
                tag_name=tag_name,
                name=title,
                message=body,
                draft=draft,
                prerelease=prerelease,
            )

            show_success(f"Release created: {release.html_url}")
            return release

        except GithubException as e:
            error_msg = e.data.get("message", str(e)) if hasattr(e, "data") else str(e)
            show_error(f"GitHub error: {error_msg}")
            return None
        except Exception as e:
            show_error(f"Failed to create release: {str(e)}")
            return None

    def get_release_by_tag(self, repo_name: str, tag_name: str):
        """Get a release by tag name."""
        try:
            user = self.github.get_user()
            repo = user.get_repo(repo_name)
            return repo.get_release(tag_name)
        except Exception:
            return None

    def list_releases(self, repo_name: str, per_page: int = 30):
        """List all releases for a repository."""
        try:
            user = self.github.get_user()
            repo = user.get_repo(repo_name)
            return list(repo.get_releases(per_page=per_page))
        except Exception as e:
            show_error(f"Failed to list releases: {str(e)}")
            return []

    def delete_release(self, repo_name: str, release_id: int) -> bool:
        """Delete a release by ID."""
        try:
            user = self.github.get_user()
            repo = user.get_repo(repo_name)
            release = repo.get_release(release_id)
            release.delete_release()
            show_success("Release deleted")
            return True
        except Exception as e:
            show_error(f"Failed to delete release: {str(e)}")
            return False
