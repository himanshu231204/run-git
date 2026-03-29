"""Configuration model for AI providers."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AIConfig:
    """Runtime configuration for AI-backed commands."""

    provider: str = "local"
    request_timeout: int = 30

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1/chat/completions"

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-haiku-latest"
    anthropic_base_url: str = "https://api.anthropic.com/v1/messages"

    # Google (Gemini)
    google_api_key: str = ""
    google_model: str = "gemini-pro"
    google_base_url: str = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    # Grok (xAI)
    grok_api_key: str = ""
    grok_model: str = "grok-beta"
    grok_base_url: str = "https://api.x.ai/v1/chat/completions"

    # Local (Ollama)
    local_model: str = "llama3.2"
    local_base_url: str = "http://localhost:11434/api/generate"

    # Common settings
    max_commit_diff_chars: int = 12000
    max_pr_diff_chars: int = 40000
    chunk_size: int = 8000
    default_base_branch: str = "main"
    default_commit_history_limit: int = 8

    @classmethod
    def from_env(cls) -> "AIConfig":
        """Build AI config from environment variables."""

        def _int_env(key: str, fallback: int) -> int:
            raw = os.getenv(key, "").strip()
            if not raw:
                return fallback
            try:
                return int(raw)
            except ValueError:
                return fallback

        return cls(
            provider=os.getenv("RUN_GIT_AI_PROVIDER", "local").strip().lower(),
            request_timeout=_int_env("RUN_GIT_AI_TIMEOUT", 30),
            openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            openai_model=os.getenv("RUN_GIT_OPENAI_MODEL", "gpt-4o-mini").strip(),
            openai_base_url=os.getenv(
                "RUN_GIT_OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions"
            ).strip(),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", "").strip(),
            anthropic_model=os.getenv(
                "RUN_GIT_ANTHROPIC_MODEL", "claude-3-5-haiku-latest"
            ).strip(),
            anthropic_base_url=os.getenv(
                "RUN_GIT_ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1/messages"
            ).strip(),
            google_api_key=os.getenv("GOOGLE_API_KEY", "").strip(),
            google_model=os.getenv(
                "RUN_GIT_GOOGLE_MODEL", "gemini-pro"
            ).strip(),
            google_base_url=os.getenv(
                "RUN_GIT_GOOGLE_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            ).strip(),
            grok_api_key=os.getenv("GROK_API_KEY", "").strip(),
            grok_model=os.getenv(
                "RUN_GIT_GROK_MODEL", "grok-beta"
            ).strip(),
            grok_base_url=os.getenv(
                "RUN_GIT_GROK_BASE_URL",
                "https://api.x.ai/v1/chat/completions"
            ).strip(),
            local_model=os.getenv("RUN_GIT_LOCAL_MODEL", "llama3.2").strip(),
            local_base_url=os.getenv(
                "RUN_GIT_LOCAL_BASE_URL",
                "http://localhost:11434/api/generate"
            ).strip(),
            max_commit_diff_chars=_int_env("RUN_GIT_MAX_COMMIT_DIFF_CHARS", 12000),
            max_pr_diff_chars=_int_env("RUN_GIT_MAX_PR_DIFF_CHARS", 40000),
            chunk_size=_int_env("RUN_GIT_DIFF_CHUNK_SIZE", 8000),
            default_base_branch=os.getenv("RUN_GIT_DEFAULT_BASE_BRANCH", "main").strip(),
            default_commit_history_limit=_int_env("RUN_GIT_COMMIT_HISTORY_LIMIT", 8),
        )