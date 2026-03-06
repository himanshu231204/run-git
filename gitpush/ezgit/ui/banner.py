"""
Banner and UI elements for gitpush
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

console = Console()

BANNER = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃                                                                    ┃
┃     ███████╗███████╗ ██████╗ ██╗████████╗                        ┃
┃     ██╔════╝╚══███╔╝██╔════╝ ██║╚══██╔══╝                        ┃
┃     █████╗    ███╔╝ ██║  ███╗██║   ██║                           ┃
┃     ██╔══╝   ███╔╝  ██║   ██║██║   ██║                           ┃
┃     ███████╗███████╗╚██████╔╝██║   ██║                           ┃
┃     ╚══════╝╚══════╝ ╚═════╝ ╚═╝   ╚═╝                           ┃
┃                                                                    ┃
┃   ═══════════════════════════════════════════════════════════     ┃
┃                                                                    ┃
┃   ⚡ Git Operations Made Effortless                               ┃
┃   🎯 One Command | Zero Hassle | Full Control                     ┃
┃                                                                    ┃
┃   ┌──────────────────────────────────────────────────────────┐   ┃
┃   │  Developer    : Himanshu Kumar                           │   ┃
┃   │  GitHub       : @himanshu231204                          │   ┃
┃   │  Repository   : github.com/himanshu231204/gitpush          │   ┃
┃   │  Version      : v1.0.0                                   │   ┃
┃   │  License      : MIT                                      │   ┃
┃   └──────────────────────────────────────────────────────────┘   ┃
┃                                                                    ┃
┃   Type 'gitpush help' to get started                                ┃
┃                                                                    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""

def show_banner():
    """Display the gitpush banner"""
    console.print(BANNER, style="bold cyan")

def show_success(message):
    """Show success message"""
    console.print(f"✅ {message}", style="bold green")

def show_error(message):
    """Show error message"""
    console.print(f"❌ {message}", style="bold red")

def show_warning(message):
    """Show warning message"""
    console.print(f"⚠️  {message}", style="bold yellow")

def show_info(message):
    """Show info message"""
    console.print(f"ℹ️  {message}", style="bold blue")

def show_progress(message):
    """Show progress message"""
    console.print(f"⏳ {message}", style="bold magenta")
