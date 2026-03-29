"""
Configuration management for gitpush.
"""
import os
import json
from typing import Optional, Dict, Any

from gitpush.exceptions import ConfigurationError


class Settings:
    """Configuration settings for gitpush."""

    DEFAULT_CONFIG = {
        'auto_pull': True,
        'auto_commit': True,
        'default_remote': 'origin',
        'default_branch': 'main',
        'commit_message_style': 'conventional',
        'auto_detect_sensitive_files': True,
        'show_progress': True,
        'color_output': True,
        # AI configuration
        'ai_provider': 'local',
        'ai_request_timeout': 30,
        'ai_openai_api_key': '',
        'ai_openai_model': 'gpt-4o-mini',
        'ai_openai_base_url': 'https://api.openai.com/v1/chat/completions',
        'ai_anthropic_api_key': '',
        'ai_anthropic_model': 'claude-3-5-haiku-latest',
        'ai_anthropic_base_url': 'https://api.anthropic.com/v1/messages',
        'ai_google_api_key': '',
        'ai_google_model': 'gemini-pro',
        'ai_google_base_url': 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
        'ai_grok_api_key': '',
        'ai_grok_model': 'grok-beta',
        'ai_grok_base_url': 'https://api.x.ai/v1/chat/completions',
        'ai_local_model': 'llama3.2',
        'ai_local_base_url': 'http://localhost:11434/api/generate',
        'ai_max_commit_diff_chars': 12000,
        'ai_max_pr_diff_chars': 40000,
        'ai_chunk_size': 8000,
        'ai_default_base_branch': 'main',
        'ai_default_commit_history_limit': 8,
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config = self.DEFAULT_CONFIG.copy()
        if os.path.exists(self.config_path):
            self.load()

    def _get_default_config_path(self) -> str:
        home = os.path.expanduser('~')
        config_dir = os.path.join(home, '.config', 'gitpush')
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, 'config.json')

    def load(self) -> None:
        try:
            with open(self.config_path, 'r') as f:
                user_config = json.load(f)
                self._config.update(user_config)
        except (json.JSONDecodeError, IOError) as e:
            raise ConfigurationError(f"Invalid config file: {e}")

    def save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            raise ConfigurationError(f"Cannot write config file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value

    def reset(self) -> None:
        self._config = self.DEFAULT_CONFIG.copy()

    def all(self) -> Dict[str, Any]:
        return self._config.copy()


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
