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
        """Show main menu and execute selected action"""
        while True:
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
                    "🌳 Commit Graph       [g] - Visual commit tree & diff",
                    "🔄 Sync              [y] - Pull & push",
                    "⚙️  Settings          [s] - Configuration",
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
            
            # Handle menu choice
            if not choice or 'Exit' in choice or 'Quit' in choice:
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                break
            
            # Execute based on selection
            if 'Quick Push' in choice:
                from gitpush.commands.push import push
                from gitpush.core.git_operations import GitOperations
                from gitpush.core.commit_generator import CommitGenerator
                from gitpush.ui.banner import show_info, show_error
                
                git_ops = GitOperations()
                if not git_ops.is_git_repo():
                    show_error("Not a git repository. Run 'run-git init' first")
                    continue
                
                if not git_ops.add_all():
                    continue
                
                generator = CommitGenerator(git_ops.repo)
                message = generator.generate_message()
                show_info(f"Auto-generated message: {message}")
                
                if not git_ops.commit(message):
                    continue
                
                git_ops.pull()
                git_ops.push()
                
            elif 'Create New Repo' in choice or 'new' in choice.lower():
                from gitpush.commands.github import new
                from click.testing import CliRunner
                runner = CliRunner()
                repo_name = questionary.text("Enter repository name:").ask()
                if repo_name:
                    result = runner.invoke(new, [repo_name, '--quick'])
                    console.print(result.output)
                    
            elif 'Clone Repo' in choice or 'clone' in choice.lower():
                from gitpush.commands.init import init_command
                from click.testing import CliRunner
                runner = CliRunner()
                url = questionary.text("Enter repository URL to clone:").ask()
                if url:
                    result = runner.invoke(init_command, [url])
                    console.print(result.output)
                    
            elif 'Branch Ops' in choice:
                InteractiveUI.branch_menu()
                
            elif 'Status/History' in choice:
                from gitpush.commands.status import status, log
                from gitpush.core.git_operations import GitOperations
                git_ops = GitOperations()
                status_data = git_ops.get_status()
                if status_data:
                    InteractiveUI.show_status_table(status_data)
                else:
                    console.print("[yellow]No changes found[/yellow]")
                    
                # Show log option
                show_log = questionary.confirm("View commit history?").ask()
                if show_log:
                    commits = git_ops.get_log(max_count=10)
                    InteractiveUI.show_log_table(commits)
            
            elif 'Commit Graph' in choice or 'Graph' in choice:
                InteractiveUI.graph_menu()
                
            elif 'Sync' in choice:
                from gitpush.core.git_operations import GitOperations
                from gitpush.ui.banner import show_info
                git_ops = GitOperations()
                show_info("Syncing with remote...")
                if git_ops.pull():
                    git_ops.push()
                    show_info("Sync complete!")
                    
            elif 'Settings' in choice or 'Configuration' in choice:
                InteractiveUI.settings_menu()
                
            elif 'Advanced Tools' in choice:
                InteractiveUI.advanced_menu()
                
            elif 'Help' in choice or 'Docs' in choice:
                from gitpush.ui.banner import show_shortcuts
                show_shortcuts()
    
    @staticmethod
    def branch_menu():
        """Show branch operations menu"""
        while True:
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
            
            if not choice or 'Back' in choice:
                break
                
            from gitpush.core.git_operations import GitOperations
            git_ops = GitOperations()
            
            if 'List' in choice:
                branches = git_ops.get_branches()
                current = git_ops.repo.active_branch.name if git_ops.is_git_repo() else "main"
                InteractiveUI.show_branches_table(branches, current)
                
            elif 'Create' in choice:
                name = questionary.text("Enter branch name:").ask()
                if name:
                    git_ops.create_branch(name)
                    console.print(f"[green]Branch '{name}' created![/green]")
                    
            elif 'Switch' in choice:
                branches = git_ops.get_branches()
                if branches:
                    selected = questionary.select("Select branch:", choices=branches).ask()
                    if selected:
                        git_ops.switch_branch(selected)
                        console.print(f"[green]Switched to '{selected}'![/green]")
                        
            elif 'Delete' in choice:
                branches = git_ops.get_branches()
                if branches:
                    selected = questionary.select("Select branch to delete:", choices=branches).ask()
                    if selected and questionary.confirm(f"Delete branch '{selected}'?").ask():
                        git_ops.delete_branch(selected)
                        console.print(f"[green]Branch '{selected}' deleted![/green]")
                        
            elif 'Merge' in choice:
                branches = git_ops.get_branches()
                if branches:
                    selected = questionary.select("Select branch to merge:", choices=branches).ask()
                    if selected:
                        try:
                            git_ops.repo.git.merge(selected)
                            console.print(f"[green]Merged '{selected}' successfully![/green]")
                        except Exception as e:
                            console.print(f"[red]Merge failed: {e}[/red]")
    
    @staticmethod
    def settings_menu():
        """Show settings menu"""
        panel = Panel(
            "[bold]Settings[/bold]\n"
            "[dim]Configure run-git[/dim]",
            title="[bold]⚙️  SETTINGS[/bold]",
            border_style="yellow",
            box=box.ROUNDED
        )
        console.print(panel)
        
        choice = questionary.select(
            "",
            choices=[
                "🎨 Theme Settings   - Change color theme",
                "📋 View Config      - Show current configuration",
                "⬅️  Back           - Return to main menu",
            ],
            qmark="➜",
            pointer="►"
        ).ask()
        
        if not choice or 'Back' in choice:
            return
            
        if 'Theme' in choice:
            from gitpush.ui.banner import ThemeManager, set_theme
            theme_choice = questionary.select(
                "Select theme:",
                choices=['default', 'dark', 'light']
            ).ask()
            set_theme(theme_choice)
            console.print(f"[green]Theme set to '{theme_choice}'![/green]")
    
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
        
        if not choice or 'Back' in choice:
            return
            
        from gitpush.core.git_operations import GitOperations
        git_ops = GitOperations()
        
        if 'Stash' in choice:
            try:
                git_ops.repo.git.stash()
                console.print("[green]Changes stashed![/green]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                
        elif 'Undo' in choice:
            if questionary.confirm("Undo last commit? (changes will be kept)").ask():
                try:
                    git_ops.repo.git.reset('HEAD~1', soft=True)
                    console.print("[green]Last commit undone![/green]")
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    
        elif 'Remote' in choice:
            remotes = git_ops.repo.remotes
            if remotes:
                for r in remotes:
                    console.print(f"  {r.name}: {r.url}")
            else:
                console.print("[yellow]No remotes configured[/yellow]")
                
        elif 'Tags' in choice:
            tags = git_ops.repo.tags
            if tags:
                for tag in tags:
                    console.print(f"  🏷️  {tag.name}")
            else:
                console.print("[yellow]No tags found[/yellow]")
                
        elif 'Logs' in choice:
            commits = git_ops.get_log(max_count=20)
            InteractiveUI.show_log_table(commits)
    
    @staticmethod
    def graph_menu():
        """Show graph/visualization menu"""
        while True:
            panel = Panel(
                "[bold]Commit Graph[/bold]\n"
                "[dim]Visualize your commit history[/dim]",
                title="[bold]🌳 COMMIT GRAPH[/bold]",
                border_style="cyan",
                box=box.ROUNDED
            )
            console.print(panel)
            
            choice = questionary.select(
                "",
                choices=[
                    "📊 Table View        - Show commits in table format",
                    "🌳 ASCII Graph       - Show branch visualization",
                    "🌿 Branch Tree       - Show branch overview",
                    "🔍 View Details      - Select commit to view details",
                    "⬅️  Back           - Return to main menu",
                ],
                qmark="➜",
                pointer="►"
            ).ask()
            
            if not choice or 'Back' in choice:
                break
            
            from gitpush.core.git_operations import GitOperations
            from gitpush.core.graph_renderer import GraphRenderer
            from gitpush.commands.graph import get_commit_details, display_commit_details
            from click.testing import CliRunner
            
            git_ops = GitOperations()
            renderer = GraphRenderer(git_ops.repo)
            
            if 'Table' in choice:
                # Show default table view
                commits = git_ops.get_log(max_count=15)
                InteractiveUI.show_log_table(commits)
                
            elif 'ASCII' in choice or 'Graph' in choice:
                runner = CliRunner()
                result = runner.invoke(
                    __import__('gitpush.commands.graph', fromlist=['graph']).graph,
                    ['--graph', '--max', '10']
                )
                console.print(result.output)
                
            elif 'Branch Tree' in choice:
                tree_output = renderer.get_branch_tree()
                console.print(tree_output)
                
            elif 'Details' in choice:
                # Show interactive commit selection
                commits = git_ops.get_log(max_count=10)
                if commits:
                    console.print("\n[bold]Select a commit to view details:[/bold]\n")
                    for i, c in enumerate(commits):
                        console.print(f"  [{i+1}] {c['hash']} | {c['message'][:50]}")
                    
                    selected = questionary.text("Enter commit number:").ask()
                    if selected and selected.isdigit():
                        idx = int(selected) - 1
                        if 0 <= idx < len(commits):
                            commit_hash = commits[idx]['hash']
                            details = get_commit_details(git_ops, renderer, commit_hash, show_diff=True)
                            if details:
                                display_commit_details(details)
    
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
