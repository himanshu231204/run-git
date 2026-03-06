"""
Main CLI interface for gitpush
"""
import click
import os
from gitpush.ui.banner import show_banner, show_success, show_error, show_warning, show_info
from gitpush.ui.interactive import InteractiveUI
from gitpush.core.git_operations import GitOperations
from gitpush.core.commit_generator import CommitGenerator
from gitpush.core.conflict_resolver import ConflictResolver
from gitpush import __version__


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', '-v', is_flag=True, help='Show version')
def main(ctx, version):
    """gitpush - Git Made Easy"""
    if version:
        click.echo(f"gitpush version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        # Show banner and interactive menu
        show_banner()
        interactive_mode()


def interactive_mode():
    """Run interactive mode"""
    git_ops = GitOperations()
    ui = InteractiveUI()
    
    while True:
        choice = ui.main_menu()
        
        if choice == "Exit":
            show_info("Thanks for using gitpush! 👋")
            break
        elif choice == "🚀 Quick Push":
            handle_quick_push(git_ops)
        elif choice == "🌿 Branch Operations":
            handle_branch_operations(git_ops, ui)
        elif choice == "📊 View Status/History":
            handle_status_history(git_ops, ui)
        elif choice == "⚙️  Configuration":
            handle_configuration(git_ops)
        elif choice == "🔧 Advanced Tools":
            handle_advanced_tools(git_ops)
        elif choice == "📚 Help & Docs":
            show_help()


def handle_quick_push(git_ops):
    """Handle quick push operation"""
    ui = InteractiveUI()
    
    # Check if git repo
    if not git_ops.is_git_repo():
        show_warning("Not a git repository!")
        if ui.confirm_action("Initialize git repository?"):
            repo_url = ui.get_repo_url()
            if git_ops.init_repo(repo_url):
                show_success("Repository initialized!")
            else:
                return
        else:
            return
    
    # Check for changes
    status = git_ops.get_status()
    if not status or not status['has_changes']:
        show_info("No changes to commit")
        return
    
    # Show status
    ui.show_status_table(status)
    
    # Check for sensitive files
    sensitive_files = git_ops.check_sensitive_files()
    if sensitive_files:
        show_warning("Sensitive files detected:")
        for file in sensitive_files:
            click.echo(f"  ⚠️  {file}")
        if not ui.confirm_action("Continue anyway?"):
            return
    
    # Add all changes
    if not git_ops.add_all():
        return
    
    # Get commit message
    commit_msg = ui.get_commit_message()
    if not commit_msg:
        generator = CommitGenerator(git_ops.repo)
        commit_msg = generator.generate_message()
        show_info(f"Auto-generated message: {commit_msg}")
    
    # Commit
    if not git_ops.commit(commit_msg):
        return
    
    # Pull
    show_info("Pulling latest changes...")
    pull_success = git_ops.pull()
    
    # Handle conflicts if any
    if not pull_success:
        resolver = ConflictResolver(git_ops.repo)
        if resolver.has_conflicts():
            if resolver.resolve_interactive():
                # Commit after resolving conflicts
                git_ops.commit(f"Merge: {commit_msg}")
            else:
                show_error("Failed to resolve conflicts")
                return
    
    # Push
    git_ops.push()


def handle_branch_operations(git_ops, ui):
    """Handle branch operations"""
    if not git_ops.is_git_repo():
        show_error("Not a git repository!")
        return
    
    choice = ui.branch_menu()
    
    if choice == "List all branches":
        branches = git_ops.get_branches()
        current = git_ops.repo.active_branch.name
        ui.show_branches_table(branches, current)
    
    elif choice == "Create new branch":
        branch_name = ui.get_branch_name()
        if git_ops.create_branch(branch_name):
            if ui.confirm_action("Switch to new branch?"):
                git_ops.switch_branch(branch_name)
    
    elif choice == "Switch branch":
        branches = git_ops.get_branches()
        branch = ui.select_branch(branches)
        if branch:
            git_ops.switch_branch(branch)
    
    elif choice == "Delete branch":
        branches = git_ops.get_branches()
        current = git_ops.repo.active_branch.name
        # Remove current branch from list
        branches = [b for b in branches if b != current]
        branch = ui.select_branch(branches)
        if branch:
            force = ui.confirm_action("Force delete (unmerged changes will be lost)?")
            git_ops.delete_branch(branch, force)
    
    elif choice == "Merge branch":
        branches = git_ops.get_branches()
        current = git_ops.repo.active_branch.name
        branches = [b for b in branches if b != current]
        branch = ui.select_branch(branches)
        if branch:
            show_info(f"Merging {branch} into {current}...")
            try:
                git_ops.repo.git.merge(branch)
                show_success(f"Successfully merged {branch}")
            except Exception as e:
                show_error(f"Merge failed: {str(e)}")
                resolver = ConflictResolver(git_ops.repo)
                if resolver.has_conflicts():
                    resolver.resolve_interactive()


def handle_status_history(git_ops, ui):
    """Handle status and history viewing"""
    if not git_ops.is_git_repo():
        show_error("Not a git repository!")
        return
    
    choice = click.prompt(
        "Choose option",
        type=click.Choice(['status', 'log', 'back']),
        default='status'
    )
    
    if choice == 'status':
        status = git_ops.get_status()
        if status:
            ui.show_status_table(status)
    
    elif choice == 'log':
        commits = git_ops.get_log(max_count=10)
        if commits:
            ui.show_log_table(commits)
        else:
            show_info("No commits yet")


def handle_configuration(git_ops):
    """Handle configuration"""
    show_info("Configuration settings")
    click.echo("\nAvailable commands:")
    click.echo("  gitpush config --set-user    Set git user info")
    click.echo("  gitpush remote              Manage remotes")


def handle_advanced_tools(git_ops):
    """Handle advanced tools"""
    show_info("Advanced tools")
    click.echo("\nAvailable commands:")
    click.echo("  gitpush stash               Stash changes")
    click.echo("  gitpush clean               Clean repository")
    click.echo("  gitpush undo                Undo last commit")


def show_help():
    """Show help information"""
    help_text = """
    [bold cyan]gitpush Commands:[/bold cyan]
    
    [yellow]Basic Commands:[/yellow]
      gitpush                    - Interactive mode
      gitpush push              - Quick push (add, commit, pull, push)
      gitpush status            - Show repository status
      gitpush log               - Show commit history
    
    [yellow]Repository:[/yellow]
      gitpush init              - Initialize repository
      gitpush init <url>        - Clone and setup repository
      gitpush remote            - Show remote repositories
      gitpush remote add <url>  - Add remote repository
    
    [yellow]Branches:[/yellow]
      gitpush branch            - List branches
      gitpush branch <name>     - Create branch
      gitpush switch <name>     - Switch to branch
      gitpush merge <name>      - Merge branch
    
    [yellow]Advanced:[/yellow]
      gitpush stash             - Stash changes
      gitpush pull              - Pull changes
      gitpush sync              - Sync with remote
    
    [yellow]Help:[/yellow]
      gitpush --help            - Show this help
      gitpush --version         - Show version
    """
    from rich.console import Console
    console = Console()
    console.print(help_text)


# Individual commands
@main.command()
@click.option('-m', '--message', help='Commit message')
@click.option('--force', is_flag=True, help='Force push')
@click.option('--dry-run', is_flag=True, help='Show what will happen')
def push(message, force, dry_run):
    """Quick push: add, commit, pull, push"""
    git_ops = GitOperations()
    
    if dry_run:
        show_info("Dry run mode - showing what will happen:")
        status = git_ops.get_status()
        if status:
            InteractiveUI.show_status_table(status)
        return
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository. Run 'gitpush init' first")
        return
    
    # Add all
    if not git_ops.add_all():
        return
    
    # Generate commit message
    if not message:
        generator = CommitGenerator(git_ops.repo)
        message = generator.generate_message()
        show_info(f"Auto-generated message: {message}")
    
    # Commit
    if not git_ops.commit(message):
        return
    
    # Pull
    git_ops.pull()
    
    # Push
    git_ops.push(force=force)


@main.command()
@click.argument('url', required=False)
def init(url):
    """Initialize git repository"""
    git_ops = GitOperations()
    
    if url:
        # Clone repository
        show_info(f"Cloning repository from {url}...")
        try:
            import git
            git.Repo.clone_from(url, '.')
            show_success("Repository cloned successfully")
        except Exception as e:
            show_error(f"Failed to clone: {str(e)}")
    else:
        # Initialize new repo
        git_ops.init_repo()
        
        # Ask for remote
        from gitpush.ui.interactive import InteractiveUI
        ui = InteractiveUI()
        if ui.confirm_action("Add remote repository?"):
            url = ui.get_repo_url()
            git_ops.add_remote("origin", url)


@main.command()
def status():
    """Show repository status"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    status = git_ops.get_status()
    if status:
        InteractiveUI.show_status_table(status)


@main.command()
@click.option('--max', default=10, help='Maximum number of commits')
@click.option('--graph', is_flag=True, help='Show graph')
def log(max, graph):
    """Show commit history"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    commits = git_ops.get_log(max_count=max)
    if commits:
        InteractiveUI.show_log_table(commits)
    else:
        show_info("No commits yet")


@main.command()
@click.argument('name', required=False)
@click.option('-d', '--delete', help='Delete branch')
def branch(name, delete):
    """Branch operations"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    if delete:
        git_ops.delete_branch(delete)
    elif name:
        git_ops.create_branch(name)
        if InteractiveUI.confirm_action("Switch to new branch?"):
            git_ops.switch_branch(name)
    else:
        branches = git_ops.get_branches()
        current = git_ops.repo.active_branch.name
        InteractiveUI.show_branches_table(branches, current)


@main.command()
@click.argument('name')
def switch(name):
    """Switch to a branch"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    git_ops.switch_branch(name)


@main.command()
@click.argument('name', required=False)
@click.option('--add', help='Add remote URL')
@click.option('--remove', is_flag=True, help='Remove remote')
def remote(name, add, remove):
    """Manage remote repositories"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    if add:
        git_ops.add_remote(name or "origin", add)
    elif remove:
        try:
            git_ops.repo.delete_remote(name or "origin")
            show_success(f"Remote '{name or 'origin'}' removed")
        except Exception as e:
            show_error(f"Failed to remove remote: {str(e)}")
    else:
        # List remotes
        remotes = git_ops.repo.remotes
        if remotes:
            show_info("Remote repositories:")
            for remote in remotes:
                click.echo(f"  {remote.name}: {remote.url}")
        else:
            show_info("No remote repositories configured")


@main.command()
def pull():
    """Pull changes from remote"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    git_ops.pull()


@main.command()
def sync():
    """Sync with remote (pull + push)"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    if git_ops.pull():
        git_ops.push()


@main.command()
@click.argument('branch')
def merge(branch):
    """Merge a branch"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    current = git_ops.repo.active_branch.name
    show_info(f"Merging {branch} into {current}...")
    
    try:
        git_ops.repo.git.merge(branch)
        show_success(f"Successfully merged {branch}")
    except Exception as e:
        show_error(f"Merge failed: {str(e)}")
        resolver = ConflictResolver(git_ops.repo)
        if resolver.has_conflicts():
            resolver.resolve_interactive()


@main.command()
def stash():
    """Stash current changes"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    try:
        git_ops.repo.git.stash()
        show_success("Changes stashed")
    except Exception as e:
        show_error(f"Failed to stash: {str(e)}")


@main.command()
def undo():
    """Undo last commit (keep changes)"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return
    
    if InteractiveUI.confirm_action("Undo last commit? (changes will be kept)"):
        try:
            git_ops.repo.git.reset('HEAD~1', soft=True)
            show_success("Last commit undone (changes kept)")
        except Exception as e:
            show_error(f"Failed to undo: {str(e)}")


if __name__ == '__main__':
    main()
