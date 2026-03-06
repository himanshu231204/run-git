"""
Interactive UI components for gitpush
"""
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


class InteractiveUI:
    """Interactive terminal UI for gitpush"""
    
    @staticmethod
    def main_menu():
        """Show main menu"""
        console.print("\n")
        panel = Panel(
            "[bold cyan]gitpush - Main Menu[/bold cyan]\n\n"
            "1. 🚀 Quick Push\n"
            "2. 🌿 Branch Operations\n"
            "3. 📊 View Status/History\n"
            "4. ⚙️  Configuration\n"
            "5. 🔧 Advanced Tools\n"
            "6. 📚 Help & Docs\n"
            "0. Exit",
            title="Choose an option",
            border_style="cyan",
            box=box.DOUBLE
        )
        console.print(panel)
        
        choice = questionary.select(
            "",
            choices=[
                "🚀 Quick Push",
                "🌿 Branch Operations",
                "📊 View Status/History",
                "⚙️  Configuration",
                "🔧 Advanced Tools",
                "📚 Help & Docs",
                "Exit"
            ]
        ).ask()
        
        return choice
    
    @staticmethod
    def branch_menu():
        """Show branch operations menu"""
        console.print("\n")
        return questionary.select(
            "Branch Operations:",
            choices=[
                "List all branches",
                "Create new branch",
                "Switch branch",
                "Delete branch",
                "Merge branch",
                "Back to main menu"
            ]
        ).ask()
    
    @staticmethod
    def get_commit_message():
        """Get commit message from user"""
        return questionary.text(
            "Enter commit message (leave empty for auto-generated):",
            default=""
        ).ask()
    
    @staticmethod
    def get_repo_url():
        """Get repository URL from user"""
        return questionary.text(
            "Enter repository URL:",
            validate=lambda text: len(text) > 0 or "URL cannot be empty"
        ).ask()
    
    @staticmethod
    def get_branch_name():
        """Get branch name from user"""
        return questionary.text(
            "Enter branch name:",
            validate=lambda text: len(text) > 0 or "Branch name cannot be empty"
        ).ask()
    
    @staticmethod
    def select_branch(branches):
        """Select a branch from list"""
        if not branches:
            console.print("[yellow]No branches available[/yellow]")
            return None
        
        return questionary.select(
            "Select a branch:",
            choices=branches
        ).ask()
    
    @staticmethod
    def confirm_action(message):
        """Confirm an action"""
        return questionary.confirm(message).ask()
    
    @staticmethod
    def show_status_table(status):
        """Display status in a table"""
        table = Table(title="Repository Status", show_header=True, header_style="bold cyan")
        table.add_column("Category", style="cyan")
        table.add_column("Files", style="yellow")
        
        table.add_row("Branch", status['branch'])
        table.add_row("Untracked", str(len(status['untracked'])))
        table.add_row("Modified", str(len(status['modified'])))
        table.add_row("Staged", str(len(status['staged'])))
        
        console.print()
        console.print(table)
        
        if status['untracked']:
            console.print("\n[bold]Untracked files:[/bold]")
            for file in status['untracked']:
                console.print(f"  [red]?[/red] {file}")
        
        if status['modified']:
            console.print("\n[bold]Modified files:[/bold]")
            for file in status['modified']:
                console.print(f"  [yellow]M[/yellow] {file}")
        
        if status['staged']:
            console.print("\n[bold]Staged files:[/bold]")
            for file in status['staged']:
                console.print(f"  [green]A[/green] {file}")
    
    @staticmethod
    def show_log_table(commits):
        """Display commit log in a table"""
        table = Table(title="Recent Commits", show_header=True, header_style="bold cyan")
        table.add_column("Hash", style="yellow")
        table.add_column("Author", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Message", style="white")
        
        for commit in commits:
            table.add_row(
                commit['hash'],
                commit['author'],
                commit['date'],
                commit['message'][:50] + "..." if len(commit['message']) > 50 else commit['message']
            )
        
        console.print()
        console.print(table)
    
    @staticmethod
    def show_branches_table(branches, current_branch):
        """Display branches in a table"""
        table = Table(title="Branches", show_header=True, header_style="bold cyan")
        table.add_column("Branch", style="cyan")
        table.add_column("Status", style="green")
        
        for branch in branches:
            status = "✓ Current" if branch == current_branch else ""
            style = "bold green" if branch == current_branch else "white"
            table.add_row(f"[{style}]{branch}[/{style}]", status)
        
        console.print()
        console.print(table)
