"""
Config command — manage run-git settings including API key.
"""

import click

from gitpush.config.settings import get_settings
from gitpush.ui.banner import console, show_error, show_success, show_warning
from gitpush.utils.license import validate_api_key_format, is_pro_user, UPGRADE_URL


@click.group(name="config")
def config_cmd():
    """Manage run-git configuration."""
    pass


@config_cmd.command(name="set-api-key")
@click.argument("api_key")
def set_api_key(api_key: str):
    """Store your PRO API key."""
    if not validate_api_key_format(api_key):
        show_error("Invalid API key format")
        console.print("  The key must start with [bold]rg_[/bold] and be at least 20 characters.")
        console.print(f"  Get a valid key from: [bold cyan]{UPGRADE_URL}[/bold cyan]")
        return

    settings = get_settings()
    settings.set("api_key", api_key)
    settings.save()

    show_success("API key saved successfully!")
    console.print("  You now have [bold]PRO[/bold] access - unlimited use of all features.")


@config_cmd.command(name="status")
def config_status():
    """Show current configuration and license status."""
    settings = get_settings()

    console.print()
    if is_pro_user():
        key = settings.get("api_key", "")
        masked = key[:6] + "..." + key[-4:] if len(key) > 10 else "****"
        console.print(f"  License:  [bold green]PRO[/bold green]  (key: {masked})")
    else:
        console.print(f"  License:  [bold yellow]FREE[/bold yellow]")
        console.print(f"  Upgrade:  [bold cyan]{UPGRADE_URL}[/bold cyan]")

    console.print(f"  Config:   [dim]{settings.config_path}[/dim]")
    console.print()


@config_cmd.command(name="remove-api-key")
def remove_api_key():
    """Remove the stored API key (downgrade to FREE)."""
    settings = get_settings()
    if settings.get("api_key"):
        settings.set("api_key", "")
        settings.save()
        show_warning("API key removed. You are now on the FREE plan.")
    else:
        console.print("  [dim]No API key was set.[/dim]")
