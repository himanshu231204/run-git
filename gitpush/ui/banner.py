"""
Banner and UI elements for run-git
"""

import sys
import time
import threading
from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from rich import box
from rich.text import Text
from rich.panel import Panel
from gitpush import __version__

# Custom theme
custom_theme = Theme(
    {
        "success": "bold green",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "bold cyan",
        "accent": "bold magenta",
        "dim": "dim",
    }
)

console = Console(theme=custom_theme, legacy_windows=False, emoji=False)


class ThemeManager:
    """Manage CLI color themes"""

    THEMES = {
        "default": {
            "primary": "cyan",
            "secondary": "green",
            "accent": "magenta",
            "success": "green",
            "error": "red",
            "warning": "yellow",
        },
        "dark": {
            "primary": "bright_cyan",
            "secondary": "bright_green",
            "accent": "bright_magenta",
            "success": "bright_green",
            "error": "bright_red",
            "warning": "bright_yellow",
        },
        "light": {
            "primary": "blue",
            "secondary": "green",
            "accent": "purple",
            "success": "green",
            "error": "red",
            "warning": "yellow",
        },
    }

    def __init__(self, theme_name="default"):
        self.theme_name = theme_name
        self.colors = self.THEMES.get(theme_name, self.THEMES["default"])

    def get(self, key):
        return self.colors.get(key, "cyan")


# Global theme instance
current_theme = ThemeManager()


def _load_saved_theme():
    """Load saved theme from config on startup"""
    try:
        from gitpush.config import get_settings
        saved_theme = get_settings().get("theme", "default")
        return ThemeManager(saved_theme)
    except Exception:
        return ThemeManager("default")


# Initialize with saved theme (if available)
current_theme = _load_saved_theme()


def set_theme(theme_name):
    """Set the color theme"""
    global current_theme
    current_theme = ThemeManager(theme_name)

    # Persist theme to config
    try:
        from gitpush.config import get_settings
        settings = get_settings()
        settings.set("theme", theme_name)
        settings.save()
    except Exception:
        pass  # Config may not be available yet

    # Refresh menu styles in interactive UI
    try:
        from gitpush.ui.interactive import refresh_menu_styles
        refresh_menu_styles()
    except Exception:
        pass


# Git Logo
GIT_LOGO = """
██████╗ ██╗   ██╗███╗   ██╗      ██████╗ ██╗████████╗
██╔══██╗██║   ██║████╗  ██║     ██╔════╝ ██║╚══██╔══╝
██████╔╝██║   ██║██╔██╗ ██║     ██║  ███╗██║   ██║   
██╔══██╗██║   ██║██║╚██╗██║     ██║   ██║██║   ██║   
██║  ██║╚██████╔╝██║ ╚████║     ╚██████╔╝██║   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═════╝ ╚═╝   ╚═╝   
"""

# Tagline
TAGLINE = "One Command • Zero Hassle • Full Control"


def get_banner(version=None):
    """Get simple banner (no animation)"""
    ver = version or __version__
    return f"""
{GIT_LOGO}
        [bold cyan]⚡ RUN-GIT ⚡[/bold cyan]
   [bold]Git Operations, Simplified[/bold]

 [dim]{TAGLINE}[/dim]
"""


def show_banner():
    """Display the run-git banner - simple version (no repeat)"""
    console.print(f"[bold cyan]{GIT_LOGO}[/bold cyan]")
    console.print(f"\n        [bold cyan]⚡ RUN-GIT ⚡[/bold cyan]")
    console.print(f"   [bold]Git Operations, Simplified[/bold]\n")
    console.print(f" [dim]{TAGLINE}[/dim]")


def show_banner_with_version():
    """Display banner with version info"""
    console.print(f"[bold cyan]{GIT_LOGO}[/bold cyan]")
    console.print(f"\n        [bold cyan]⚡ RUN-GIT ⚡[/bold cyan]")
    console.print(f"   [bold]Git Operations, Simplified[/bold]\n")
    console.print(f" [dim]{TAGLINE}[/dim]\n")
    console.print(f" [dim]v{__version__}[/dim]")


def show_success(message):
    """Show success message"""
    console.print(f"[OK]  {message}", style=f"bold {current_theme.colors['success']}")


def show_error(message):
    """Show error message"""
    console.print(f"[X]  {message}", style=f"bold {current_theme.colors['error']}")


def show_warning(message):
    """Show warning message"""
    console.print(f"[!]  {message}", style=f"bold {current_theme.colors['warning']}")


def show_info(message):
    """Show info message"""
    console.print(f"[i]  {message}", style=f"bold {current_theme.colors['primary']}")


def show_progress(message):
    """Show progress message"""
    console.print(f"[*] {message}", style=f"bold {current_theme.colors['accent']}")


def show_step(step, total, message):
    """Show progress step (e.g., 2/4)"""
    console.print(
        f"[{current_theme.colors['primary']}][{step}/{total}][/{current_theme.colors['primary']}] {message}"
    )


def show_keyhint(keys):
    """Show keyboard shortcuts hint"""
    hints = " | ".join([f"[bold]{k}[/]: {v}" for k, v in keys])
    console.print(f"[{current_theme.colors['dim']}]{hints}[/{current_theme.colors['dim']}]")


# Loading spinner for operations
class Spinner:
    """Animated spinner for long operations"""

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message="Loading"):
        self.message = message
        self.frame = 0
        self.running = False

    def __enter__(self):
        self.running = True
        return self

    def __exit__(self, *args):
        self.running = False
        console.print("")

    def update(self, message=None):
        """Update spinner frame"""
        if message:
            self.message = message
        frame = self.FRAMES[self.frame % len(self.FRAMES)]
        print(f"\r{frame} {self.message}", end="", flush=True)
        self.frame += 1


def loading_spinner(func):
    """Decorator for spinner on functions"""

    def wrapper(*args, **kwargs):
        with Spinner("Processing..."):
            return func(*args, **kwargs)

    return wrapper


# Colorized git status
def colorize_status(status):
    """Return colorized status text"""
    colors = {
        "added": current_theme.colors["success"],
        "modified": current_theme.colors["warning"],
        "deleted": current_theme.colors["error"],
        "untracked": current_theme.colors["primary"],
        "renamed": current_theme.colors["accent"],
    }

    def colorize(text, status_type):
        color = colors.get(status_type, "white")
        return f"[{color}]{text}[/{color}]"

    return colorize


# Command suggestion
def show_suggestion(command, explanation):
    """Show command suggestion"""
    console.print(f"→ Did you mean: [bold cyan]{command}[/]? {explanation}")


# Keyboard shortcut display
KEYBOARD_SHORTCUTS = {
    "?": "Show help",
    "h": "Help menu",
    "q": "Quit",
    "r": "Refresh",
    "p": "Quick push",
    "s": "Status",
    "g": "Commit graph",
    "b": "Branch menu",
    "c": "Cancel",
    "enter": "Confirm",
    "esc": "Go back",
}


def show_shortcuts():
    """Show available keyboard shortcuts"""
    from rich.table import Table
    from rich.panel import Panel
    from gitpush.ui.help_docs import MENU_SHORTCUTS

    primary = current_theme.colors["primary"]
    
    table = Table(show_header=True, header_style=f"bold {primary}")
    table.add_column("Key", style="yellow", width=8)
    table.add_column("Action", style="white")
    table.add_column("Description", style="dim")

    # Get main menu shortcuts from help_docs
    shortcuts = MENU_SHORTCUTS.get("main_menu", {}).get("items", [])
    for key, action, description in shortcuts:
        table.add_row(f"[bold]{key}[/bold]", action, description)

    panel = Panel(
        table,
        title=f"[{primary}]⌨  Keyboard Shortcuts[/{primary}]",
        border_style=primary,
        box=box.ROUNDED,
    )
    console.print(panel)


def clear_screen():
    """Clear the terminal screen"""
    console.clear()
