"""
Theme command for gitpush.
"""
import click
from rich.console import Console
from gitpush.ui.banner import set_theme, current_theme, ThemeManager, show_success

console = Console()


@click.command()
@click.argument('theme_name', required=False, type=click.Choice(['default', 'dark', 'light', 'list']))
def theme(theme_name):
    """Manage color themes (default, dark, light)"""
    if not theme_name or theme_name == 'list':
        console.print("\n[bold cyan]Available themes:[/bold cyan]")
        for name in ThemeManager.THEMES:
            marker = "*" if name == current_theme.theme_name else " "
            console.print(f"  {marker} {name}")
        console.print("\n[dim]Usage: run-git theme [theme-name][/dim]")
        return
    
    set_theme(theme_name)
    console.print(f"[green]Theme set to: {theme_name}[/green]")


# Import console for local usage
console = Console()
