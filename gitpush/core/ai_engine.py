"""Core AI orchestration for commit/pr/review features."""

from __future__ import annotations

import os
from typing import Optional

from gitpush.ai.client import AIClient
from gitpush.ai.config import AIConfig
from gitpush.core.git_operations import GitOperations
from gitpush.exceptions import AIDiffError, NotARepositoryError
from gitpush.utils.diff_cleaner import DiffCleaner
from gitpush.config.settings import get_settings


class AIEngine:
    """Coordinate Git input, diff cleaning, and AI generation."""

    def __init__(
        self,
        git_ops: Optional[GitOperations] = None,
        ai_client: Optional[AIClient] = None,
        diff_cleaner: Optional[DiffCleaner] = None,
        config: Optional[AIConfig] = None,
    ) -> None:
        if config is None:
            settings = get_settings()
            # Helper to get value from environment or settings with fallback
            def _get_value(env_key: str, settings_key: str, default: str = "") -> str:
                value = os.getenv(env_key)
                if value is None:
                    value = settings.get(settings_key)
                if value is None:
                    return default
                return value.strip()

            # Helper to get integer value from environment or settings with fallback
            def _get_int_value(env_key: str, settings_key: str, default: int) -> int:
                value = os.getenv(env_key)
                if value is None:
                    value = settings.get(settings_key)
                if value is None:
                    return default
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return default

            config_dict = {
                "provider": _get_value(
                    "RUN_GIT_AI_PROVIDER",
                    "ai_provider",
                    "local"
                ).lower(),
                "request_timeout": _get_int_value(
                    "RUN_GIT_AI_TIMEOUT",
                    "ai_request_timeout",
                    30
                ),
                "openai_api_key": _get_value(
                    "OPENAI_API_KEY",
                    "ai_openai_api_key",
                    ""
                ),
                "openai_model": _get_value(
                    "RUN_GIT_OPENAI_MODEL",
                    "ai_openai_model",
                    "gpt-4o-mini"
                ),
                "openai_base_url": _get_value(
                    "RUN_GIT_OPENAI_BASE_URL",
                    "ai_openai_base_url",
                    "https://api.openai.com/v1/chat/completions"
                ),
                "anthropic_api_key": _get_value(
                    "ANTHROPIC_API_KEY",
                    "ai_anthropic_api_key",
                    ""
                ),
                "anthropic_model": _get_value(
                    "RUN_GIT_ANTHROPIC_MODEL",
                    "ai_anthropic_model",
                    "claude-3-5-haiku-latest"
                ),
                "anthropic_base_url": _get_value(
                    "RUN_GIT_ANTHROPIC_BASE_URL",
                    "ai_anthropic_base_url",
                    "https://api.anthropic.com/v1/messages"
                ),
                "google_api_key": _get_value(
                    "GOOGLE_API_KEY",
                    "ai_google_api_key",
                    ""
                ),
                "google_model": _get_value(
                    "RUN_GIT_GOOGLE_MODEL",
                    "ai_google_model",
                    "gemini-pro"
                ),
                "google_base_url": _get_value(
                    "RUN_GIT_GOOGLE_BASE_URL",
                    "ai_google_base_url",
                    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                ),
                "grok_api_key": _get_value(
                    "GROK_API_KEY",
                    "ai_grok_api_key",
                    ""
                ),
                "grok_model": _get_value(
                    "RUN_GIT_GROK_MODEL",
                    "ai_grok_model",
                    "grok-beta"
                ),
                "grok_base_url": _get_value(
                    "RUN_GIT_GROK_BASE_URL",
                    "ai_grok_base_url",
                    "https://api.x.ai/v1/chat/completions"
                ),
                "local_model": _get_value(
                    "RUN_GIT_LOCAL_MODEL",
                    "ai_local_model",
                    "llama3.2"
                ),
                "local_base_url": _get_value(
                    "RUN_GIT_LOCAL_BASE_URL",
                    "ai_local_base_url",
                    "http://localhost:11434/api/generate"
                ),
                "max_commit_diff_chars": _get_int_value(
                    "RUN_GIT_MAX_COMMIT_DIFF_CHARS",
                    "ai_max_commit_diff_chars",
                    12000
                ),
                "max_pr_diff_chars": _get_int_value(
                    "RUN_GIT_MAX_PR_DIFF_CHARS",
                    "ai_max_pr_diff_chars",
                    40000
                ),
                "chunk_size": _get_int_value(
                    "RUN_GIT_DIFF_CHUNK_SIZE",
                    "ai_chunk_size",
                    8000
                ),
                "default_base_branch": _get_value(
                    "RUN_GIT_DEFAULT_BASE_BRANCH",
                    "ai_default_base_branch",
                    "main"
                ),
                "default_commit_history_limit": _get_int_value(
                    "RUN_GIT_COMMIT_HISTORY_LIMIT",
                    "ai_default_commit_history_limit",
                    8
                ),
            }
            config = AIConfig(**config_dict)

        self.config = config
        self.git_ops = git_ops or GitOperations()
        self.ai_client = ai_client or AIClient(config=self.config)
        self.diff_cleaner = diff_cleaner or DiffCleaner()

    def generate_commit_message(self) -> str:
        """Generate conventional commit message from staged/fallback diff."""

        self._ensure_repo()

        raw_diff = self.git_ops.get_staged_diff()
        if not raw_diff.strip():
            raw_diff = self.git_ops.get_working_diff()

        cleaned = self._prepare_diff(
            raw_diff=raw_diff,
            max_chars=self.config.max_commit_diff_chars,
        )
        return self.ai_client.generate_commit_message(cleaned)

    def generate_pr_description(
        self,
        base_branch: Optional[str] = None,
        head_ref: str = "HEAD",
        commit_limit: Optional[int] = None,
    ) -> str:
        """Generate PR description from branch diff and commit history."""

        self._ensure_repo()

        resolved_base = base_branch or self.config.default_base_branch
        raw_diff = self.git_ops.get_branch_diff(base_branch=resolved_base, head_ref=head_ref)
        cleaned = self._prepare_diff(raw_diff=raw_diff, max_chars=self.config.max_pr_diff_chars)
        limit = commit_limit or self.config.default_commit_history_limit
        commit_messages = self.git_ops.get_recent_commit_messages(limit=limit)

        return self.ai_client.generate_pr_description(cleaned, commit_messages)

    def generate_review(self, base_branch: Optional[str] = None, head_ref: str = "HEAD") -> str:
        """Generate AI review feedback from branch diff."""

        self._ensure_repo()

        resolved_base = base_branch or self.config.default_base_branch
        raw_diff = self.git_ops.get_branch_diff(base_branch=resolved_base, head_ref=head_ref)
        cleaned = self._prepare_diff(raw_diff=raw_diff, max_chars=self.config.max_pr_diff_chars)

        return self.ai_client.generate_review(cleaned)

    def _prepare_diff(self, raw_diff: str, max_chars: int) -> str:
        prepared = self.diff_cleaner.prepare_for_ai(
            raw_diff=raw_diff,
            max_chars=max_chars,
            chunk_size=self.config.chunk_size,
        )
        if self.diff_cleaner.is_empty(prepared):
            raise AIDiffError("No diff content found for AI analysis")
        return prepared

    def _ensure_repo(self) -> None:
        if not self.git_ops.is_git_repo():
            raise NotARepositoryError("Not a git repository")
