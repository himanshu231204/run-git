"""
Main CLI interface for run-git
"""
import click
import os
import questionary
from git import Repo, InvalidGitRepositoryError
from gitpush.ui.banner import show_banner, show_progress, show_success, show_error, show_warning, show_info
from gitpush.ui.interactive import InteractiveUI
from gitpush.core.git_operations import GitOperations
from gitpush.core.commit_generator import CommitGenerator
from gitpush.core.conflict_resolver import ConflictResolver
from gitpush import __version__


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', '-v', is_flag=True, help='Show version')
def main(ctx, version):
    """run-git - Git Made Easy"""
    if version:
        click.echo(f"run-git version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        # Show banner and interactive menu
        show_banner()
        interactive_mode()


# ========================================
# - interactive_mode() function
# ========================================


def interactive_mode():
    """Run interactive mode"""
    git_ops = GitOperations()
    ui = InteractiveUI()
    
    while True:
        choice = ui.main_menu()
        
        if choice == "Exit":
            show_info("Thanks for using run-git! 👋")
            break
        elif choice == "🚀 Quick Push":
            handle_quick_push(git_ops)
        elif choice == "🆕 Create New Repo":  # ← NEW HANDLER
            handle_create_repo(git_ops)
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






def handle_create_repo(git_ops):
    """
    Production-ready GitHub repo creation + push
    Works with EMPTY remote repo (no conflicts)
    """

    from gitpush.core.github_manager import GitHubManager
    from git import Repo, InvalidGitRepositoryError, GitCommandError
    import glob
    import os

    gh = GitHubManager()
    ui = InteractiveUI()

    # ============================================================
    # STEP 1: AUTH
    # ============================================================
    if not gh.authenticate():
        return

    # ============================================================
    # STEP 2: CHECK LOCAL REPO
    # ============================================================
    is_existing_repo = False

    try:
        local_repo = Repo('.')
        is_existing_repo = True
        show_warning("Already a git repository")

        if 'origin' in [r.name for r in local_repo.remotes]:
            show_info(f"Remote: {local_repo.remote('origin').url}")

            if not ui.confirm_action("Replace remote with new repo?"):
                return
        else:
            if not ui.confirm_action("Connect this repo to GitHub?"):
                return

    except InvalidGitRepositoryError:
        files = [f for f in (glob.glob('*') + glob.glob('.*'))
                 if f not in ['.', '..', '.git']]

        if files:
            show_info(f"\n📂 Found {len(files)} file(s)")
            for f in files[:5]:
                show_info(f"   • {f}")

            if len(files) > 5:
                show_info(f"   ... +{len(files) - 5} more")

            if not ui.confirm_action("Create repo with these files?"):
                return

    # ============================================================
    # STEP 3: USER INPUT
    # ============================================================
    repo_name = questionary.text("Repository name:").ask()
    if not repo_name:
        return

    description = questionary.text("Description:", default="").ask()
    visibility = questionary.select(
        "Visibility:", choices=['Public', 'Private']
    ).ask()

    # Gitignore
    detected = gh.detect_language()
    use_detected = questionary.confirm(
        f"Use {detected} gitignore?"
    ).ask()

    gitignore = detected if use_detected else None

    # License
    licenses = gh.get_license_templates()
    license_key = questionary.select(
        "License:", choices=list(licenses.keys())
    ).ask()

    create_readme = questionary.confirm("Create README?").ask()

    config = {
        "name": repo_name,
        "description": description,
        "private": (visibility == 'Private')
    }

    if not questionary.confirm("Create repository?").ask():
        return

    # ============================================================
    # STEP 4: CREATE EMPTY GITHUB REPO
    # ============================================================
    github_repo = gh.create_repository(config)
    if not github_repo:
        return

    # ============================================================
    # STEP 5: INIT LOCAL
    # ============================================================
    if not is_existing_repo:
        show_progress("Initializing repo...")
        local_repo = Repo.init('.')

    # ============================================================
    # STEP 6: CREATE FILES LOCALLY
    # ============================================================

    # .gitignore
    if gitignore and not os.path.exists('.gitignore'):
        content = gh.get_gitignore_content(gitignore)
        if content:
            with open('.gitignore', 'w') as f:
                f.write(content)

    # LICENSE
    if license_key != 'None' and not os.path.exists('LICENSE'):
        user = gh.github.get_user()
        content = gh.get_license_content(
            licenses[license_key],
            user.name or user.login
        )
        if content:
            with open('LICENSE', 'w') as f:
                f.write(content)

    # README
    if create_readme and not os.path.exists('README.md'):
        user = gh.github.get_user()

        with open('README.md', 'w') as f:
            f.write(f"# {repo_name}\n\n{description}\n")

    # ============================================================
    # STEP 7: REMOTE SETUP
    # ============================================================
    remote_url = github_repo.clone_url.strip()

    if 'origin' in [r.name for r in local_repo.remotes]:
        local_repo.delete_remote('origin')

    local_repo.create_remote('origin', remote_url)

    # ============================================================
    # STEP 8: ADD + COMMIT
    # ============================================================
    local_repo.git.add(A=True)

    staged = local_repo.git.diff('--cached', '--name-only').split('\n')
    staged = [f for f in staged if f]

    if staged:
        try:
            local_repo.head.commit
            msg = f"Add files to {repo_name}"
        except:
            msg = "Initial commit"

        local_repo.index.commit(msg)
        show_success(f"Committed: {msg}")
    else:
        show_warning("Nothing to commit")

    # ============================================================
    # STEP 9: BRANCH FIX
    # ============================================================
    try:
        current = local_repo.active_branch.name
    except:
        current = None

    if current != 'main':
        local_repo.git.branch('-M', 'main')

    # ============================================================
    # STEP 10: PUSH (FINAL FIXED LOGIC)
    # ============================================================
    show_progress("Pushing...")

    origin = local_repo.remote('origin')
    success = False

    try:
        origin.push(refspec='main:main', set_upstream=True)
        success = True
        show_success("Push successful")

    except GitCommandError:
        show_warning("Push failed, retrying with pull...")

        try:
            local_repo.git.pull(
                'origin', 'main',
                '--allow-unrelated-histories',
                '--no-edit'
            )

            origin.push(refspec='main:main', set_upstream=True)
            success = True
            show_success("Push successful after sync")

        except Exception as e:
            show_error(f"Push failed: {str(e)}")

    # ============================================================
    # FINAL OUTPUT
    # ============================================================
    print("\n" + "=" * 60)

    if success:
        show_success("🎉 Repo created & pushed!")
        show_info(f"🔗 {github_repo.html_url}")
    else:
        show_warning("Repo created but push failed")
        show_info(f"🔗 {github_repo.html_url}")

    print("=" * 60 + "\n")




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
    click.echo("  run-git config --set-user    Set git user info")
    click.echo("  run-git remote              Manage remotes")


def handle_advanced_tools(git_ops):
    """Handle advanced tools"""
    show_info("Advanced tools")
    click.echo("\nAvailable commands:")
    click.echo("  run-git stash               Stash changes")
    click.echo("  run-git clean               Clean repository")
    click.echo("  run-git undo                Undo last commit")


def show_help():
    """Show help information"""
    help_text = """
    [bold cyan]RUN-GIT Commands:[/bold cyan]
    
    [yellow]Basic Commands:[/yellow]
      run-git                    - Interactive mode
      run-git push              - Quick push (add, commit, pull, push)
      run-git status            - Show repository status
      run-git log               - Show commit history
    
    [yellow]Repository:[/yellow]
      run-git init              - Initialize repository
      run-git init <url>        - Clone and setup repository
       run-git new <name>        - Create new GitHub repository ← NEW!
      run-git remote            - Show remote repositories
      run-git remote add <url>  - Add remote repository
    
    [yellow]Branches:[/yellow]
      run-git branch            - List branches
      run-git branch <name>     - Create branch
      run-git switch <name>     - Switch to branch
      run-git merge <name>      - Merge branch
    
    [yellow]Advanced:[/yellow]
      run-git stash             - Stash changes
      run-git pull              - Pull changes
      run-git sync              - Sync with remote
    
    [yellow]Help:[/yellow]
      run-git --help            - Show this help
      run-git --version         - Show version
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
        show_error("Not a git repository. Run 'run-git init' first")
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



# ========================================
# STEP 4: FIXING init COMMAND
# ========================================


@main.command()
@click.argument('url', required=False)
def init(url):
    """Initialize git repository"""
    git_ops = GitOperations()
    
    if url:
        # Clone repository
        show_info(f"Cloning repository from {url}...")
        try:
            Repo.clone_from(url, '.')  # ← CHANGED: git.Repo → Repo
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



# ========================================
#  COMMAND TO github_manager.py
# ========================================


@main.command()
@click.argument('repo_name', required=True)
@click.option('--description', '-d', help='Repository description')
@click.option('--private', is_flag=True, help='Make repository private')
@click.option('--public', is_flag=True, help='Make repository public (default)')
@click.option('--gitignore', '-g', help='Gitignore template (e.g., Python, Node)')
@click.option('--license', '-l', help='License (MIT, Apache-2.0, GPL-3.0)')
@click.option('--no-readme', is_flag=True, help='Skip README creation')
@click.option('--quick', is_flag=True, help='Use smart defaults, no prompts')
def new(repo_name, description, private, public, gitignore, license, no_readme, quick):
    """Create a new GitHub repository"""
    from gitpush.core.github_manager import GitHubManager
    
    gh = GitHubManager()
    
    # Authenticate
    if not gh.authenticate():
        return
    
    # Check if already a git repo
    try:
        repo = Repo('.')
        show_error("This directory is already a git repository!")
        show_info(f"Remote: {repo.remotes.origin.url if repo.remotes else 'None'}")
        return
    except InvalidGitRepositoryError:
        pass  # Good, not a git repo
    
    # Build configuration
    config = {'name': repo_name}
    
    if quick:
        # Smart defaults
        show_info("Using smart defaults...")
        config['description'] = description or f"Created with run-git"
        config['private'] = False
        config['gitignore'] = gh.detect_language()
        config['license'] = 'mit'
        config['readme'] = True
        
        show_info(f"Language detected: {config['gitignore']}")
        show_info(f"License: MIT")
        show_info(f"Visibility: Public")
        
    else:
        # Interactive prompts
        show_info("\n📝 Repository Configuration")
        
        # Description
        if not description:
            description = questionary.text(
                "Repository description:",
                default=""
            ).ask()
        config['description'] = description
        
        # Visibility
        if not private and not public:
            visibility = questionary.select(
                "Repository visibility:",
                choices=['Public', 'Private']
            ).ask()
            config['private'] = (visibility == 'Private')
        else:
            config['private'] = private
        
        # Gitignore
        if not gitignore:
            detected = gh.detect_language()
            show_info(f"Detected language: {detected}")
            
            use_detected = questionary.confirm(
                f"Use {detected} gitignore template?"
            ).ask()
            
            if use_detected:
                config['gitignore'] = detected
            else:
                templates = gh.get_gitignore_templates()
                gitignore = questionary.select(
                    "Select gitignore template:",
                    choices=['None'] + templates
                ).ask()
                config['gitignore'] = None if gitignore == 'None' else gitignore
        else:
            config['gitignore'] = gitignore
        
        # License
        if not license:
            licenses = gh.get_license_templates()
            license_choice = questionary.select(
                "Select license:",
                choices=list(licenses.keys())
            ).ask()
            config['license'] = licenses[license_choice]
        else:
            config['license'] = license.lower()
        
        # README
        config['readme'] = not no_readme
        if not no_readme and not quick:
            config['readme'] = questionary.confirm(
                "Create README.md?"
            ).ask()
    
    # Summary
    show_info("\n📋 Summary:")
    show_info(f"  Name: {config['name']}")
    show_info(f"  Description: {config.get('description', 'None')}")
    show_info(f"  Visibility: {'Private' if config.get('private') else 'Public'}")
    show_info(f"  Gitignore: {config.get('gitignore', 'None')}")
    show_info(f"  License: {config.get('license', 'None')}")
    show_info(f"  README: {'Yes' if config.get('readme') else 'No'}")
    
    if not quick:
        confirm = questionary.confirm("\nCreate repository?").ask()
        if not confirm:
            show_info("Cancelled")
            return
    
    # Create on GitHub
    github_repo = gh.create_repository(config)
    if not github_repo:
        return
    
    # Initialize local repository
    show_progress("Initializing local repository...")
    local_repo = Repo.init('.')
    
    # Create .gitignore
    if config.get('gitignore'):
        show_progress("Creating .gitignore...")
        gitignore_content = gh.get_gitignore_content(config['gitignore'])
        if gitignore_content:
            with open('.gitignore', 'w') as f:
                f.write(gitignore_content)
            show_success(".gitignore created")
    
    # Create LICENSE
    if config.get('license'):
        show_progress("Creating LICENSE...")
        user = gh.github.get_user()
        license_content = gh.get_license_content(
            config['license'],
            user.name or user.login
        )
        if license_content:
            with open('LICENSE', 'w') as f:
                f.write(license_content)
            show_success("LICENSE created")
    
    # Create README
    if config.get('readme'):
        show_progress("Creating README.md...")
        user = gh.github.get_user()
        readme_content = f"""# {config['name']}

{config.get('description', '')}

## Installation

```bash
# Add installation instructions
```

## Usage

```bash
# Add usage examples
```

## Author

{user.name or user.login} ([@{user.login}](https://github.com/{user.login}))

## License

{config.get('license', 'MIT').upper() if config.get('license') else 'All rights reserved'}
"""
        with open('README.md', 'w') as f:
            f.write(readme_content)
        show_success("README.md created")
    
    # Add remote
    show_progress("Adding remote origin...")
    local_repo.create_remote('origin', github_repo.clone_url)
    
    # Initial commit
    show_progress("Creating initial commit...")
    local_repo.git.add(A=True)
    local_repo.index.commit("Initial commit")
    
    # Ensure branch is main
    
    local_repo.git.branch('-M', 'main')
    
    # Push to GitHub
    show_progress("Pushing to GitHub...")
    origin = local_repo.remote('origin')
    
    try:
        origin.push('main')

    except Exception:
                 show_warning("Push failed. Attempting to sync with remote...")

    try:
        local_repo.git.pull('origin', 'main', '--allow-unrelated-histories')
        origin.push('main')
        show_success("Repository synced and pushed successfully!")

    except Exception as e:
        show_error(f"Push failed after retry: {str(e)}")
        return   
    
    
    

    
    # Success!
    show_success("\n🎉 Repository created successfully!")
    show_info(f"🔗 {github_repo.html_url}")
    show_info(f"📂 Local: {os.getcwd()}")
    show_info("\nNext steps:")
    show_info("  1. Add your code")
    show_info("  2. run-git push")

if __name__ == '__main__':
    main()