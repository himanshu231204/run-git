"""Factory for creating AI providers."""
from __future__ import annotations

from gitpush.ai.config import AIConfig
from gitpush.ai.providers.anthropic import AnthropicProvider
from gitpush.ai.providers.base import BaseAIProvider
from gitpush.ai.providers.google import GoogleProvider
from gitpush.ai.providers.grok import GrokProvider
from gitpush.ai.providers.local import LocalAIProvider
from gitpush.ai.providers.openai import OpenAIProvider
from gitpush.exceptions import AIConfigurationError


class AIProviderFactory:
    """Create AI providers based on runtime configuration."""

    @staticmethod
    def create(config: AIConfig) -> BaseAIProvider:
        provider = config.provider.lower().strip()

        if provider == "openai":
            if not config.openai_api_key:
                raise AIConfigurationError("OPENAI_API_KEY is required for OpenAI provider")
            return OpenAIProvider(
                api_key=config.openai_api_key,
                model=config.openai_model,
                base_url=config.openai_base_url,
                timeout=config.request_timeout,
            )

        if provider == "anthropic":
            if not config.anthropic_api_key:
                raise AIConfigurationError("ANTHROPIC_API_KEY is required for Anthropic provider")
            return AnthropicProvider(
                api_key=config.anthropic_api_key,
                model=config.anthropic_model,
                base_url=config.anthropic_base_url,
                timeout=config.request_timeout,
            )

        if provider == "google":
            if not config.google_api_key:
                raise AIConfigurationError("GOOGLE_API_KEY is required for Google provider")
            return GoogleProvider(
                api_key=config.google_api_key,
                model=config.google_model,
                base_url=config.google_base_url,
                timeout=config.request_timeout,
            )

        if provider == "grok":
            if not config.grok_api_key:
                raise AIConfigurationError("GROK_API_KEY is required for Grok provider")
            return GrokProvider(
                api_key=config.grok_api_key,
                model=config.grok_model,
                base_url=config.grok_base_url,
                timeout=config.request_timeout,
            )

        if provider == "local":
            return LocalAIProvider(
                model=config.local_model,
                base_url=config.local_base_url,
                timeout=config.request_timeout,
            )

        raise AIConfigurationError(
            "Unsupported provider. Use one of: openai, anthropic, google, grok, local"
        )