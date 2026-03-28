"""
Interactive UI components for gitpush
"""
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich import box
from rich.style import Style
from gitpush.ui.banner import current_theme, show_shortcuts

console = Console()


class InteractiveUI:
    """Interactive terminal UI for gitpush"""
    
    @staticmethod
    def main_menu():
        """Show main menu with enhanced UI"""
        console.print("\n")
        
        # Header
        panel = Panel(
            "[bold cyan]Welcome to run-git[/bold cyan]\n"
            "[dim]Git operations made effortless[/dim]\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            title="[bold]🚀 MAIN MENU[/bold]",
            border_style="cyan",
            box=box.DOUBLE
        )
        console.print(panel)
        
        choice = questionary.select(
            "",
            choices=[
                "🚀 Quick Push          [p] - Push changes instantly",
                "🆕 Create New Repo    [n] - Create GitHub repository", 
                "📥 Clone Repo         [c] - Clone existing repository",
                "🌿 Branch Ops         [b] - Branch management",
                "📊 Status/History     [s] - View status & logs",
                "🔄 Sync              [y] - Pull & push",
                "⚙️  Settings          [g] - Configuration",
                "🔧 Advanced Tools     [a] - Stash, undo, etc.",
                "📚 Help & Docs        [h] - Keyboard shortcuts",
                "[red]❌ Exit           [q] - Quit application[/red]",
            ],
            qmark="➜",
            pointer="►",
            style=questionary.Style([
                ('selected', 'fg:cyan bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
            ])
        ).ask()
        
        # Extract choice index
        choices_map = {
            0: 'push',
            1: 'new',
            2: 'clone',
            3: 'branch',
            4: 'status',
            5: 'sync',
            6: 'settings',
            7: 'advanced',
            8: 'help',
            9: 'exit',
        }
        
        return choice
    
    @staticmethod
    def branch_menu():
        """Show branch operations menu with shortcuts"""
        panel = Panel(
            "[bold]Branch Operations[/bold]\n"
            "[dim]Manage your branches easily[/dim]",
            title="[bold]🌿 BRANCH OPERATIONS[/bold]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(panel)
        
        choice = questionary.select(
            "",
            choices=[
                "📋 List Branches    [l] - View all branches",
                "➕ Create Branch   [n] - Create new branch",
                "🔄 Switch Branch   [s] - Switch to branch",
                "🗑️  Delete Branch  [d] - Delete a branch",
                "🔀 Merge Branch   [m] - Merge branch",
                "⬅️  Back           [b] - Return to main menu",
            ],
            qmark="➜",
            pointer="►"
        ).ask()
        
        return choice
    
    @staticmethod
    def advanced_menu():
        """Show advanced tools menu"""
        panel = Panel(
            "[bold]Advanced Tools[/bold]\n"
            "[dim]Power user features[/dim]",
            title="[bold]🔧 ADVANCED TOOLS[/bold]",
            border_style="magenta",
            box=box.ROUNDED
        )
        console.print(panel)
        
        choice = questionary.select(
            "",
            choices=[
                "📦 Stash Changes    - Temporarily save changes",
                "↩️  Undo Commit     - Revert last commit",
                "🔗 Remote Mgmt     - Manage remotes",
                "🏷️  Tags           - List/create tags",
                "📜 View Logs       - Detailed commit history",
                "⬅️  Back           - Return to main menu",
            ],
            qmark="➜",
            pointer="►"
        ).ask()
        
        return choice
    
    @staticmethod
    def get_commit_message():
        """Get commit message with better UI"""
        return questionary.text(
            "📝 Enter commit message (leave empty for auto-generated):",
            default="",
            qmark="➜",
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
            ])
        ).ask()
    
    @staticmethod
    def get_repo_url():
        """Get repository URL with validation"""
        return questionary.text(
            "🔗 Enter repository URL:",
            validate=lambda text: len(text) > 0 or "URL cannot be empty",
            qmark="➜"
        ).ask()
    
    @staticmethod
    def get_branch_name():
        """Get branch name with validation"""
        return questionary.text(
            "🌿 Enter branch name:",
            validate=lambda text: len(text) > 0 or "Branch name cannot be empty",
            qmark="➜"
        ).ask()
    
    @staticmethod
    def select_branch(branches):
        """Select a branch from list"""
        if not branches:
            console.print("[yellow]⚠️  No branches available[/yellow]")
            return None
        
        return questionary.select(
            "🌿 Select a branch:",
            choices=branches,
            qmark="➜",
            pointer="►"
        ).ask()
    
    @staticmethod
    def confirm_action(message):
        """Confirm an action with better styling"""
        return questionary.confirm(
            f"❓ {message}",
            qmark="➜",
            style=questionary.Style([
                ('qmark', 'fg:cyan bold'),
                ('answer', 'fg:green bold'),
            ])
        ).ask()
    
    @staticmethod
    def show_status_table(status):
        """Display status in enhanced table"""
        table = Table(
            title="📊 Repository Status",
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors['primary'],
            box=box.ROUNDED
        )
        table.add_column("📁 Category", style=f"{current_theme.colors['primary']}", width=20)
        table.add_column("📄 Files", style=f"{current_theme.colors['warning']}", justify="right")
        
        table.add_row("🌿 Branch", f"[bold]{status.get('branch', 'N/A')}[/bold]")
        table.add_row("🆕 Untracked", f"[yellow]{len(status.get('untracked', []))}[/yellow]")
        table.add_row("✏️  Modified", f"[yellow]{len(status.get('modified', []))}[/yellow]")
        table.add_row("✅ Staged", f"[green]{len(status.get('staged', []))}[/green]")
        
        console.print()
        console.print(table)
        
        # File details
        if status.get('untracked'):
            console.print(f"\n[bold yellow]🆕 Untracked files:[/bold yellow]")
            for file in status['untracked']:
                console.print(f"   [red]?[/red]  {file}")
        
        if status.get('modified'):
            console.print(f"\n[bold yellow]✏️  Modified files:[/bold yellow]")
            for file in status['modified']:
                console.print(f"   [yellow]M[/yellow]  {file}")
        
        if status.get('staged'):
            console.print(f"\n[bold green]✅ Staged files:[/bold green]")
            for file in status['staged']:
                console.print(f"   [green]A[/green]  {file}")
    
    @staticmethod
    def show_log_table(commits):
        """Display commit log in enhanced table"""
        table = Table(
            title="📜 Recent Commits",
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors['primary'],
            box=box.ROUNDED
        )
        table.add_column("🏷️  Hash", style=f"{current_theme.colors['warning']}", width=8)
        table.add_column("👤 Author", style=f"{current_theme.colors['primary']}", width=15)
        table.add_column("📅 Date", style=f"{current_theme.colors['success']}", width=12)
        table.add_column("💬 Message", style="white")
        
        for commit in commits:
            msg = commit.get('message', '')
            truncated = msg[:50] + "..." if len(msg) > 50 else msg
            table.add_row(
                f"[yellow]{commit.get('hash', '')[:7]}[/yellow]",
                commit.get('author', 'Unknown')[:15],
                commit.get('date', '')[:10],
                truncated
            )
        
        console.print()
        console.print(table)
    
    @staticmethod
    def show_branches_table(branches, current_branch):
        """Display branches in enhanced table"""
        table = Table(
            title="🌿 Branches",
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors['primary'],
            box=box.ROUNDED
        )
        table.add_column("🌿 Branch", style="white")
        table.add_column("📍 Status", style=f"{current_theme.colors['success']}", justify="center")
        
        for branch in branches:
            is_current = branch == current_branch
            status = "✓ Current" if is_current else ""
            style = f"bold {current_theme.colors['success']}" if is_current else "white"
            indicator = "► " if is_current else "  "
            
            table.add_row(
                f"[{style}]{indicator}{branch}[/{style}]",
                status
            )
        
        console.print()
        console.print(table)
    
    @staticmethod
    def show_progress_bar(description="Processing..."):
        """Create a progress bar for long operations"""
        progress = Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            console=console,
        )
        return progress


# Command suggestions based on common mistakes
COMMAND_SUGGESTIONS = {
    'git push': 'run-git push',
    'git commit': 'run-git push (includes commit)',
    'git status': 'run-git status',
    'git log': 'run-git log',
    'git branch': 'run-git branch',
    'git checkout': 'run-git switch',
    'git pull': 'run-git pull',
    'git clone': 'run-git init',
}


def suggest_command(misspelled):
    """Suggest correct command"""
    from gitpush.ui.banner import show_suggestion
    
    for wrong, correct in COMMAND_SUGGESTIONS.items():
        if wrong in misspelled.lower():
            show_suggestion(correct, "is the run-git equivalent")
            return True
    return False
