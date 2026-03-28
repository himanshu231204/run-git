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
custom_theme = Theme({
    "success": "bold green",
    "error": "bold red",
    "warning": "bold yellow",
    "info": "bold cyan",
    "accent": "bold magenta",
    "dim": "dim",
})

console = Console(theme=custom_theme)


class ThemeManager:
    """Manage CLI color themes"""
    
    THEMES = {
        'default': {
            'primary': 'cyan',
            'secondary': 'green', 
            'accent': 'magenta',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
        },
        'dark': {
            'primary': 'bright_cyan',
            'secondary': 'bright_green', 
            'accent': 'bright_magenta',
            'success': 'bright_green',
            'error': 'bright_red',
            'warning': 'bright_yellow',
        },
        'light': {
            'primary': 'blue',
            'secondary': 'green',
            'accent': 'purple',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
        },
    }
    
    def __init__(self, theme_name='default'):
        self.theme_name = theme_name
        self.colors = self.THEMES.get(theme_name, self.THEMES['default'])
    
    def get(self, key):
        return self.colors.get(key, 'cyan')


# Global theme instance
current_theme = ThemeManager()


def set_theme(theme_name):
    """Set the color theme"""
    global current_theme
    current_theme = ThemeManager(theme_name)


# Git Logo
GIT_LOGO = """
██████╗ ██╗   ██╗███╗   ██╗      ██████╗ ██╗████████╗
██╔══██╗██║   ██║████╗  ██║     ██╔════╝ ██║╚══██╔══╝
██████╔╝██║   ██║██╔██╗ ██║     ██║  ███╗██║   ██║   
██╔══██╗██║   ██║██║╚██╗██║     ██║   ██║██║   ██║   
██║  ██║╚██████╔╝██║ ╚████║     ╚██████╔╝██║   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═════╝ ╚═╝   ╚═╝   
"""

# Animated RUN-GIT text
RUN_GIT_TEXT = [
    ["⚡ RUN-GIT ⚡", "cyan"],
    ["⚡ RUN-GIT ⚡", "magenta"],
    ["⚡ RUN-GIT ⚡", "green"],
    ["⚡ RUN-GIT ⚡", "yellow"],
    ["⚡ RUN-GIT ⚡", "cyan"],
]

# Subtitle
SUBTITLE = "Git Operations, Simplified"

# Tagline
TAGLINE = "One Command • Zero Hassle • Full Control"


def get_banner(version=None, animated=False):
    """Get professional banner"""
    ver = version or __version__
    return f"""
{GIT_LOGO}
        [bold cyan]⚡ RUN-GIT ⚡[/bold cyan]
   [bold]Git Operations, Simplified[/bold]

 [dim]One Command • Zero Hassle • Full Control[/dim]
"""


def show_banner():
    """Display the run-git banner with animation"""
    # Show Git logo
    console.print(f"[bold cyan]{GIT_LOGO}[/bold cyan]")
    
    # Animated RUN-GIT text
    for text, color in RUN_GIT_TEXT:
        console.clear()
        console.print(f"[bold cyan]{GIT_LOGO}[/bold cyan]")
        console.print(f"\n        [bold {color}]{text}[/bold {color}]")
        console.print(f"   [bold]Git Operations, Simplified[/bold]\n")
        console.print(f" [dim]{TAGLINE}[/dim]")
        time.sleep(0.15)
    
    # Final banner (stays on screen)
    console.print(f"\n        [bold cyan]⚡ RUN-GIT ⚡[/bold cyan]")
    console.print(f"   [bold]Git Operations, Simplified[/bold]\n")
    console.print(f" [dim]{TAGLINE}[/dim]")


def show_banner_simple():
    """Display simple non-animated banner"""
    console.print(f"[bold cyan]{GIT_LOGO}[/bold cyan]")
    console.print(f"\n        [bold cyan]⚡ RUN-GIT ⚡[/bold cyan]")
    console.print(f"   [bold]Git Operations, Simplified[/bold]\n")
    console.print(f" [dim]{TAGLINE}[/dim]")


def show_success(message):
    """Show success message"""
    console.print(f"✓  {message}", style=f"bold {current_theme.colors['success']}")


def show_error(message):
    """Show error message"""
    console.print(f"✗  {message}", style=f"bold {current_theme.colors['error']}")


def show_warning(message):
    """Show warning message"""
    console.print(f"⚠  {message}", style=f"bold {current_theme.colors['warning']}")


def show_info(message):
    """Show info message"""
    console.print(f"ℹ  {message}", style=f"bold {current_theme.colors['primary']}")


def show_progress(message):
    """Show progress message"""
    console.print(f"⟳ {message}", style=f"bold {current_theme.colors['accent']}")


def show_step(step, total, message):
    """Show progress step (e.g., 2/4)"""
    console.print(f"[{current_theme.colors['primary']}][{step}/{total}][/{current_theme.colors['primary']}] {message}")


def show_keyhint(keys):
    """Show keyboard shortcuts hint"""
    hints = " | ".join([f"[bold]{k}[/]: {v}" for k, v in keys])
    console.print(f"[{current_theme.colors['dim']}]{hints}[/{current_theme.colors['dim']}]")


# Loading spinner for operations
class Spinner:
    """Animated spinner for long operations"""
    
    FRAMES = [
        "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
    ]
    
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
        'added': current_theme.colors['success'],
        'modified': current_theme.colors['warning'],
        'deleted': current_theme.colors['error'],
        'untracked': current_theme.colors['primary'],
        'renamed': current_theme.colors['accent'],
    }
    
    def colorize(text, status_type):
        color = colors.get(status_type, 'white')
        return f"[{color}]{text}[/{color}]"
    
    return colorize


# Command suggestion
def show_suggestion(command, explanation):
    """Show command suggestion"""
    console.print(f"→ Did you mean: [bold cyan]{command}[/]? {explanation}")


# Keyboard shortcut display
KEYBOARD_SHORTCUTS = {
    '?': 'Show help',
    'h': 'Help menu', 
    'q': 'Quit',
    'r': 'Refresh',
    'p': 'Quick push',
    's': 'Status',
    'b': 'Branch menu',
    'c': 'Cancel',
    'enter': 'Confirm',
    'esc': 'Go back',
}


def show_shortcuts():
    """Show available keyboard shortcuts"""
    from rich.table import Table
    from rich.panel import Panel
    
    table = Table(show_header=True, header_style=f"bold {current_theme.colors['primary']}")
    table.add_column("Key", style="yellow", width=8)
    table.add_column("Action", style="white")
    
    for key, action in KEYBOARD_SHORTCUTS.items():
        table.add_row(f"[bold]{key}[/]", action)
    
    panel = Panel(
        table,
        title=f"[{current_theme.colors['primary']}]⌨  Keyboard Shortcuts[/{current_theme.colors['primary']}]",
        border_style=current_theme.colors['primary'],
        box=box.ROUNDED
    )
    console.print(panel)


def clear_screen():
    """Clear the terminal screen"""
    console.clear()
