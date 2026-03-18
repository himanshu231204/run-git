
"""
GitHub integration for run-git
Handles repo creation, authentication, and GitHub API operations
PRODUCTION READY VERSION (Fixed push conflicts + improved API handling)
"""

import os
import yaml
import requests
from pathlib import Path
from github import Github, GithubException
import questionary
from gitpush.ui.banner import (
    show_success, show_error, show_warning, show_info, show_progress
)


class GitHubManager:
    """Manage GitHub operations"""

    CONFIG_DIR = Path.home() / '.run-git'
    CONFIG_FILE = CONFIG_DIR / 'config.yml'

    def __init__(self):
        self.token = None
        self.github = None
        self._load_config()

    # ============================================================
    # CONFIG HANDLING
    # ============================================================
    def _load_config(self):
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r') as f:
                    config = yaml.safe_load(f)
                    self.token = config.get('github_token')
                    if self.token:
                        self.github = Github(self.token)
        except Exception as e:
            show_warning(f"Could not load config: {str(e)}")

    def _save_config(self):
        try:
            self.CONFIG_DIR.mkdir(exist_ok=True)
            config = {'github_token': self.token}

            with open(self.CONFIG_FILE, 'w') as f:
                yaml.dump(config, f)

            os.chmod(self.CONFIG_FILE, 0o600)
            show_success("GitHub token saved securely")

        except Exception as e:
            show_error(f"Failed to save config: {str(e)}")

    # ============================================================
    # AUTHENTICATION
    # ============================================================
    def authenticate(self):
        """Authenticate with GitHub"""

        if self.token and self.github:
            try:
                user = self.github.get_user()
                _ = user.login  # force API call
                return True
            except Exception:
                show_warning("Saved token is invalid")
                self.token = None

        show_info("\nGitHub Personal Access Token required")
        show_info("Create one at: https://github.com/settings/tokens")
        show_info("Scopes: repo, user")

        token = questionary.password("Enter your GitHub token:").ask()

        if not token:
            show_error("Token is required")
            return False

        try:
            gh = Github(token)
            user = gh.get_user().login

            show_success(f"Authenticated as: {user}")

            self.token = token
            self.github = gh
            self._save_config()
            return True

        except Exception as e:
            show_error(f"Authentication failed: {str(e)}")
            return False

    # ============================================================
    # REPOSITORY HELPERS
    # ============================================================
    def repo_exists(self, repo_name):
        try:
            user = self.github.get_user()
            user.get_repo(repo_name)
            return True
        except:
            return False

    def suggest_repo_name(self, base_name):
        counter = 1
        while True:
            new_name = f"{base_name}-{counter}"
            if not self.repo_exists(new_name):
                return new_name
            counter += 1
            if counter > 10:
                import time
                return f"{base_name}-{int(time.time())}"

    # ============================================================
    # LANGUAGE DETECTION
    # ============================================================
    def detect_language(self):
        if Path('requirements.txt').exists() or Path('setup.py').exists():
            return 'Python'
        elif Path('package.json').exists():
            return 'Node'
        elif Path('pom.xml').exists() or Path('build.gradle').exists():
            return 'Java'
        elif Path('go.mod').exists():
            return 'Go'
        elif Path('Cargo.toml').exists():
            return 'Rust'
        elif Path('Gemfile').exists():
            return 'Ruby'
        elif Path('composer.json').exists():
            return 'PHP'
        return 'Python'

    # ============================================================
    # CREATE REPOSITORY (CRITICAL FIX HERE)
    # ============================================================
    def create_repository(self, config):
        """
        Create EMPTY GitHub repository

        IMPORTANT:
        - No gitignore_template
        - No license_template
        - No auto_init
        """

        try:
            user = self.github.get_user()

            # Check if repo exists
            if self.repo_exists(config['name']):
                show_warning(f"Repository '{config['name']}' already exists")

                suggestion = self.suggest_repo_name(config['name'])
                show_info(f"Suggested: {suggestion}")

                use = questionary.confirm(
                    f"Use '{suggestion}' instead?"
                ).ask()

                if use:
                    config['name'] = suggestion
                else:
                    return None

            show_progress(f"Creating repository '{config['name']}'...")

            # 🔥 CRITICAL: EMPTY REPO CREATION
            repo = user.create_repo(
                name=config['name'],
                description=config.get('description', ''),
                private=config.get('private', False),
                auto_init=False,   # MUST
                has_issues=True,
                has_wiki=True,
                has_downloads=True
            )

            show_success(f"Repository created: {repo.html_url}")
            return repo

        except GithubException as e:
            show_error(f"GitHub Error: {e.data.get('message', str(e))}")
            return None

        except Exception as e:
            show_error(f"Unexpected error: {str(e)}")
            return None

    # ============================================================
    # CONTENT FETCHERS
    # ============================================================
    def get_gitignore_content(self, template):
        try:
            url = f"https://api.github.com/gitignore/templates/{template}"

            headers = {
                'Authorization': f'Bearer {self.token}'
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json().get('source', '')
            else:
                show_warning(f"Gitignore fetch failed: {response.status_code}")
                return None

        except Exception as e:
            show_warning(f"Gitignore error: {str(e)}")
            return None

    def get_license_content(self, license_key, author_name):
        try:
            url = f"https://api.github.com/licenses/{license_key}"

            response = requests.get(url)

            if response.status_code == 200:
                content = response.json().get('body', '')

                import datetime
                year = datetime.datetime.now().year

                content = content.replace('[year]', str(year))
                content = content.replace('[fullname]', author_name)

                return content
            else:
                show_warning(f"License fetch failed: {response.status_code}")
                return None

        except Exception as e:
            show_warning(f"License error: {str(e)}")
            return None
