
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
    CONFIG_DIR = Path.home() / '.run-git'
    CONFIG_FILE = CONFIG_DIR / 'config.yml'

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
                with open(self.CONFIG_FILE, 'r') as f:
                    config = yaml.safe_load(f)
                    self.token = config.get('github_token')
                    if self.token:
                        self.github = Github(self.token)
        except Exception as e:
            show_warning(f"Config load failed: {str(e)}")

    def _save_config(self):
        try:
            self.CONFIG_DIR.mkdir(exist_ok=True)

            with open(self.CONFIG_FILE, 'w') as f:
                yaml.dump({'github_token': self.token}, f)

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
            'Python', 'Node', 'Java', 'Go', 'Rust',
            'C++', 'C', 'Ruby', 'PHP', 'Swift',
            'Kotlin', 'Dart', 'R'
        ]

    def get_license_templates(self):
        return {
            'MIT': 'mit',
            'Apache 2.0': 'apache-2.0',
            'GPL v3': 'gpl-3.0',
            'BSD 3-Clause': 'bsd-3-clause',
            'ISC': 'isc',
            'None': None
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
        if Path('requirements.txt').exists():
            return 'Python'
        elif Path('package.json').exists():
            return 'Node'
        elif Path('pom.xml').exists():
            return 'Java'
        return 'Python'

    # ============================================================
    # 🔥 FIXED CREATE REPO (EMPTY REPO)
    # ============================================================
    def create_repository(self, config):
        """
        Create EMPTY GitHub repository (NO FILES)
        """

        try:
            user = self.github.get_user()

            # Check exists
            if self.repo_exists(config['name']):
                show_warning("Repo exists")

                new_name = self.suggest_repo_name(config['name'])
                show_info(f"Suggested: {new_name}")

                if questionary.confirm(f"Use {new_name}?").ask():
                    config['name'] = new_name
                else:
                    return None

            show_progress(f"Creating '{config['name']}'...")

            repo = user.create_repo(
                name=config['name'],
                description=config.get('description', ''),
                private=config.get('private', False),
                auto_init=False,   # 🔥 CRITICAL
                has_issues=True,
                has_wiki=True,
                has_downloads=True
            )

            show_success(f"Created: {repo.html_url}")
            return repo

        except GithubException as e:
            show_error(f"GitHub error: {e.data.get('message', str(e))}")
            return None

        except Exception as e:
            show_error(str(e))
            return None

    # ============================================================
    # CONTENT FETCH
    # ============================================================
    def get_gitignore_content(self, template):
        try:
            url = f"https://api.github.com/gitignore/templates/{template}"
            headers = {"Authorization": f"Bearer {self.token}"}

            r = requests.get(url, headers=headers)

            if r.status_code == 200:
                return r.json().get('source', '')
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
                text = r.json().get('body', '')

                import datetime
                year = str(datetime.datetime.now().year)

                text = text.replace('[year]', year)
                text = text.replace('[fullname]', author)

                return text
            else:
                show_warning(f"License failed: {r.status_code}")
                return None

        except Exception as e:
            show_warning(str(e))
            return None

