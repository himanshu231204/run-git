"""
License and feature gating for run-git.

Feature tiers:
  FREE  — commit-ai (5/day), pr-ai (2/day), review-ai (3/day)
  PRO   — unlimited access to all features

Usage counters are stored in the config file under "usage".
"""

from __future__ import annotations

import webbrowser
from datetime import date
from typing import Optional

import click

from gitpush.config.settings import get_settings
from gitpush.ui.banner import console, show_info

# ── Constants ────────────────────────────────────────────────────────────────

UPGRADE_URL = "https://run-git.com"

# feature name → (tier, daily_free_limit)
# tier "pro"   = PRO-only (no free usage)
# tier "free"  = free with a daily limit
FEATURE_TIERS: dict[str, tuple[str, int]] = {
    "commit-ai": ("free", 5),
    "pr-ai": ("free", 2),
    "review-ai": ("free", 3),
}

API_KEY_PREFIX = "rg_"
API_KEY_MIN_LENGTH = 20


# ── Helpers ──────────────────────────────────────────────────────────────────

def _today() -> str:
    return str(date.today())


def _get_usage(settings) -> dict:
    """Return today's usage counters from config.

    Resets all counters when the date changes.
    """
    usage = settings.get("usage", {})
    if usage.get("date") != _today():
        return {"date": _today(), **{f: 0 for f in FEATURE_TIERS}}
    return usage


def _save_usage(settings, usage: dict) -> None:
    settings.set("usage", usage)
    settings.save()


def get_api_key() -> Optional[str]:
    """Return the stored API key, or None."""
    key = get_settings().get("api_key")
    if key and isinstance(key, str) and key.strip():
        return key.strip()
    return None


def is_pro_user() -> bool:
    """True when a valid-looking API key is configured."""
    key = get_api_key()
    return (
        key is not None
        and key.startswith(API_KEY_PREFIX)
        and len(key) >= API_KEY_MIN_LENGTH
    )


def validate_api_key_format(key: str) -> bool:
    """Basic format check — must start with rg_ and be at least 20 chars."""
    return (
        isinstance(key, str)
        and key.startswith(API_KEY_PREFIX)
        and len(key) >= API_KEY_MIN_LENGTH
    )


# ── Upgrade prompt ───────────────────────────────────────────────────────────

def _show_upgrade_prompt(feature: str, tier: str) -> None:
    """Show the upgrade message and optionally open the browser."""
    console.print()

    if tier == "pro":
        console.print(f"  [bold yellow]{feature}[/bold yellow] is a PRO feature.")
    else:
        console.print(
            f"  You've reached the daily free limit for "
            f"[bold yellow]{feature}[/bold yellow]."
        )

    console.print()
    console.print("  To unlock unlimited access:")
    console.print(f"  Get your API key from:  [bold cyan]{UPGRADE_URL}[/bold cyan]")
    console.print()
    console.print("  Then run:")
    console.print("  [bold green]  run-git config set-api-key YOUR_KEY[/bold green]")
    console.print()

    try:
        if click.confirm("  Do you want to open the website now?", default=True):
            webbrowser.open(UPGRADE_URL)
            show_info("Opening browser...")
    except (click.Abort, EOFError):
        pass


# ── Public gate function ─────────────────────────────────────────────────────

def check_feature_access(feature: str) -> int:
    """Check whether the current user may use *feature*.

    Returns the number of remaining free uses (>= 0) if allowed.
    Returns -1 if blocked (upgrade prompt was shown).
    PRO users always get -1 (unlimited, no counter shown).
    """
    if feature not in FEATURE_TIERS:
        return -1  # unknown feature — allow, no counter

    tier, daily_limit = FEATURE_TIERS[feature]

    # PRO users: always allowed, no counter
    if is_pro_user():
        return -1

    settings = get_settings()
    usage = _get_usage(settings)
    used = usage.get(feature, 0)

    # PRO-only feature, no key
    if tier == "pro":
        _show_upgrade_prompt(feature, tier)
        return -1

    # Free tier — over limit
    if used >= daily_limit:
        _show_upgrade_prompt(feature, tier)
        return -1

    # Allowed — increment and return remaining
    usage[feature] = used + 1
    _save_usage(settings, usage)
    return daily_limit - (used + 1)
