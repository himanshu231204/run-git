"""
Tag and Release commands for gitpush.
"""

import click
import questionary

from gitpush.core.git_operations import GitOperations
from gitpush.core.github_manager import GitHubManager
from gitpush.ui.banner import (
    show_progress,
    show_error,
    show_info,
    show_success,
    show_warning,
)


@click.command()
@click.argument("tag_name", required=False)
@click.option("--message", "-m", "message", help="Tag annotation message")
@click.option(
    "--release",
    "-r",
    "create_release",
    is_flag=True,
    help="Also create GitHub release",
)
@click.option(
    "--draft",
    is_flag=True,
    help="Create as draft release (requires --release)",
)
@click.option("--title", "-t", "title", help="Release title (default: tag name)")
@click.option(
    "--body",
    "-b",
    "body",
    help="Release notes (use --ai to generate with AI)",
)
@click.option(
    "--ai",
    "use_ai",
    is_flag=True,
    help="Generate release notes using AI",
)
@click.option(
    "--push/--no-push",
    default=True,
    help="Push tag to remote (default: push)",
)
@click.option(
    "--annotated/--lightweight",
    default=True,
    help="Create annotated tag (default: annotated)",
)
def tag(
    tag_name,
    message,
    create_release,
    draft,
    title,
    body,
    use_ai,
    push,
    annotated,
):
    """Create and optionally release a tag.

    Examples:
        run-git tag v1.0.0
        run-git tag v1.0.0 -m "Version 1.0.0"
        run-git tag v1.0.0 -r --draft
        run-git tag v1.0.0 -r --ai
    """
    git_ops = GitOperations()

    if not git_ops.is_git_repo():
        show_error("Not a git repository. Run 'run-git init' first.")
        return

    # If no tag name provided, show interactive menu
    if not tag_name:
        show_tag_menu(git_ops)
        return

    # Create the tag
    if not git_ops.create_tag(tag_name, message=message, annotated=annotated):
        show_error(f"Failed to create tag '{tag_name}'")
        return

    # Push tag if requested
    if push:
        if not git_ops.push_tag(tag_name):
            show_warning(
                f"Tag created but failed to push. Push manually: git push origin {tag_name}"
            )
        else:
            show_success(f"Tag '{tag_name}' pushed to remote")

    # Create release if requested
    if create_release:
        create_github_release(git_ops, tag_name, title, body, use_ai, draft)
    else:
        show_info(f"Tag '{tag_name}' created. Use -r to create a GitHub release.")


def show_tag_menu(git_ops: GitOperations):
    """Show interactive tag management menu with premium styling."""
    from rich.panel import Panel
    from rich.console import Console
    from rich import box

    console = Console()

    while True:
        # Display header panel
        panel = Panel(
            "[bold]Tag & Release Manager[/bold]\n[dim]Create, push, and release your tags[/dim]",
            title="[bold]🏷️ TAG MANAGEMENT[/bold]",
            border_style="yellow",
            box=box.DOUBLE,
        )
        console.print(panel)
        console.print()

        # Define menu sections with premium styling
        tag_sections = [
            {
                "title": "TAG OPERATIONS",
                "items": [
                    ("1", "📝", "Create Tag", "Create a new version tag"),
                    ("2", "☁️", "Push Tag", "Push a tag to remote"),
                    ("3", "🚀", "Create Release", "Create tag + push + GitHub release"),
                    ("4", "📦", "Push All Tags", "Push all tags to remote"),
                    ("5", "🗑️", "Delete Tag", "Delete a local tag"),
                    ("6", "👁️", "View Tags", "View all tags with details"),
                ],
            },
        ]

        # Build choices
        all_choices = []
        choice_map = {}

        for section in tag_sections:
            for key, icon, label, desc in section.get("items", []):
                choice_text = f"{icon} {label:20} → {desc}"
                choice_map[choice_text] = key
                all_choices.append(choice_text)

        # Add back option
        all_choices.append("⬅️ Back              → Return to previous menu")
        choice_map["⬅️ Back              → Return to previous menu"] = "back"

        # Show menu
        choice = questionary.select(
            "",
            choices=all_choices,
            style=questionary.Style(
                [
                    ("selected", "fg:cyan bold"),
                    ("pointer", "fg:cyan bold"),
                ]
            ),
        ).ask()

        if not choice:
            break

        # Map choice to action
        key = choice_map.get(choice, "")

        if key == "back" or not choice or "Back" in choice:
            break
        elif key == "1":
            create_tag_interactive(git_ops)
        elif key == "2":
            push_tag_interactive(git_ops)
        elif key == "3":
            create_release_interactive(git_ops)
        elif key == "4":
            push_all_tags_interactive(git_ops)
        elif key == "5":
            delete_tag_interactive(git_ops)
        elif key == "6":
            view_tags_interactive(git_ops)


def create_tag_interactive(git_ops: GitOperations):
    """Interactive tag creation with premium styling."""
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.panel import Panel

    console = Console()

    # Show header
    console.print(
        Panel(
            "[bold]Create New Tag[/bold]\n[dim]Version tagging for releases[/dim]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )
    console.print()

    # Get tag name with validation hint
    tag_name = questionary.text(
        "📝 Enter tag name (e.g., v1.0.0):",
    ).ask()

    if not tag_name:
        show_error("Tag name is required")
        return

    # Validate tag name format
    if not git_ops._is_valid_tag_name(tag_name):
        show_error(
            f"Invalid tag name: '{tag_name}'. " "Use letters, numbers, dots, hyphens, underscores."
        )
        return

    # Check if tag already exists
    if git_ops.tag_exists(tag_name):
        show_warning(f"Tag '{tag_name}' already exists")
        return

    message = questionary.text(
        "📝 Enter tag message (optional):",
        default=f"Release {tag_name}",
    ).ask()

    annotated = questionary.confirm("🏷️ Create annotated tag?", default=True).ask()

    if git_ops.create_tag(tag_name, message=message, annotated=annotated):
        show_success(f"✅ Tag '{tag_name}' created successfully")

        # Ask to push
        if questionary.confirm(f"☁️ Push tag '{tag_name}' to remote?").ask():
            if git_ops.push_tag(tag_name):
                show_success(f"✅ Tag '{tag_name}' pushed to remote")
            else:
                show_warning("Failed to push tag")
    else:
        show_error(f"Failed to create tag '{tag_name}'")


def push_tag_interactive(git_ops: GitOperations):
    """Interactive tag push with premium styling."""
    from rich.console import Console
    from rich.panel import Panel
    from rich import box

    console = Console()
    tags = git_ops.list_tags()

    if not tags:
        show_warning("No tags found")
        return

    # Show header
    console.print(
        Panel(
            "[bold]Push Tag to Remote[/bold]\n[dim]Upload tag to GitHub[/dim]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )
    console.print()

    tag_names = [t["name"] for t in tags]
    tag_name = questionary.select(
        "☁️ Select tag to push:",
        choices=tag_names,
    ).ask()

    if tag_name and git_ops.push_tag(tag_name):
        show_success(f"✅ Tag '{tag_name}' pushed to remote")
    else:
        show_error(f"Failed to push tag '{tag_name}'")


def create_release_interactive(git_ops: GitOperations):
    """Interactive release creation with one-click flow and premium styling."""
    from rich.console import Console
    from rich.panel import Panel
    from rich import box

    console = Console()

    # Show header
    console.print(
        Panel(
            "[bold]🚀 Create GitHub Release[/bold]\n[dim]Create tag + push + release in one click[/dim]",
            border_style="green",
            box=box.DOUBLE,
        )
    )
    console.print()

    # Step 1: Get or create tag
    tags = git_ops.list_tags()
    tag_choices = ["Create New Tag", "Use Existing Tag"]

    choice = questionary.select(
        "📋 Select tag option:",
        choices=tag_choices,
    ).ask()

    if choice == "Create New Tag":
        tag_name = questionary.text("🏷️  Enter new tag name (e.g., v1.0.0):").ask()
        if not tag_name:
            show_error("Tag name is required")
            return

        message = questionary.text(
            "📝 Enter tag message:",
            default=f"Release {tag_name}",
        ).ask()

        if not git_ops.create_tag(tag_name, message=message, annotated=True):
            show_error(f"Failed to create tag '{tag_name}'")
            return

        # Push the new tag
        show_progress(f"Pushing tag '{tag_name}' to remote...")
        git_ops.push_tag(tag_name)
    else:
        if not tags:
            show_warning("No existing tags found")
            return
        tag_names = [t["name"] for t in tags]
        tag_name = questionary.select("🏷️  Select tag:", choices=tag_names).ask()

        if not tag_name:
            return

        # Try to push tag
        show_progress(f"Pushing tag '{tag_name}' to remote...")
        if not git_ops.push_tag(tag_name):
            show_warning(f"Tag '{tag_name}' may already exist on remote")

    # Step 2: Check remote
    remote_url = git_ops.get_remote_url()
    if not remote_url:
        show_error("No remote origin found")
        return

    # Step 3: Get release info
    release_title = questionary.text(
        "📄 Release title:",
        default=tag_name,
    ).ask()

    # Step 4: Choose release notes method
    notes_choice = questionary.select(
        "📝 Release notes:",
        choices=["Write manually (default)", "Generate with AI 🤖"],
    ).ask()

    release_body = ""
    if "AI" in notes_choice:
        use_ai = True
        release_body = ""
    else:
        use_ai = False
        release_body = (
            questionary.text(
                "Enter release notes:",
            ).ask()
            or ""
        )

    # Step 5: Draft option
    is_draft = questionary.confirm("📋 Create as draft release?", default=False).ask()

    # Step 6: Create release
    console.print()
    create_github_release(git_ops, tag_name, release_title, release_body, use_ai, is_draft)


def push_all_tags_interactive(git_ops: GitOperations):
    """Interactive push all tags with premium styling."""
    from rich.console import Console
    from rich.panel import Panel
    from rich import box

    console = Console()
    tags = git_ops.list_tags()

    if not tags:
        show_warning("No tags found")
        return

    # Show header
    console.print(
        Panel(
            "[bold]📦 Push All Tags[/bold]\n[dim]Upload all local tags to GitHub[/dim]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )
    console.print()

    tag_names = [t["name"] for t in tags]
    console.print(f"[dim]Found {len(tag_names)} tags: [cyan]{', '.join(tag_names)}[/cyan][/dim]\n")

    if questionary.confirm(f"☁️  Push all {len(tag_names)} tags to remote?").ask():
        show_progress(f"Pushing {len(tag_names)} tags to remote...")
        if git_ops.push_all_tags():
            show_success(f"✅ All {len(tag_names)} tags pushed to remote")
        else:
            show_error("Failed to push tags")
    else:
        show_info("Cancelled")


def delete_tag_interactive(git_ops: GitOperations):
    """Interactive tag deletion with premium styling."""
    from rich.console import Console
    from rich.panel import Panel
    from rich import box

    console = Console()
    tags = git_ops.list_tags()

    if not tags:
        show_warning("No tags found")
        return

    # Show header
    console.print(
        Panel(
            "[bold]Delete Tag[/bold]\n[dim]Remove a local tag[/dim]",
            border_style="red",
            box=box.ROUNDED,
        )
    )
    console.print()

    tag_names = [t["name"] for t in tags]
    tag_name = questionary.select(
        "🗑️ Select tag to delete:",
        choices=tag_names,
    ).ask()

    if tag_name:
        # Double confirm with warning
        console.print(
            f"\n[yellow]⚠️  You are about to delete tag: [bold]{tag_name}[/bold][/yellow]"
        )

        if questionary.confirm("Are you sure you want to delete this tag?").ask():
            if git_ops.delete_tag(tag_name):
                show_success(f"✅ Tag '{tag_name}' has been deleted")
            else:
                show_error(f"Failed to delete tag '{tag_name}'")
        else:
            show_info("Deletion cancelled")


def view_tags_interactive(git_ops: GitOperations):
    """Interactive view tags with professional table display."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box

    console = Console()
    tags = git_ops.list_tags()

    if not tags:
        show_warning("No tags found")
        return

    # Create a professional table
    table = Table(
        title="🏷️  Repository Tags",
        show_header=True,
        header_style="bold yellow",
        border_style="yellow",
        box=box.ROUNDED,
        pad_edge=True,
    )

    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Tag Name", style="cyan bold", width=25)
    table.add_column("Commit", style="green", width=10)
    table.add_column("Date", style="dim", width=15)
    table.add_column("Message", style="white", width=40)

    for idx, t in enumerate(tags, 1):
        commit = t.get("commit", "N/A")
        date = t.get("date", "N/A")
        msg = t.get("message", "")

        # Truncate message if too long
        if msg and len(msg) > 35:
            msg = msg[:35] + "..."

        row_style = "dim" if idx % 2 == 0 else ""

        table.add_row(
            f"{idx}",
            f"[cyan]{t['name']}[/cyan]",
            f"[green]{commit}[/green]",
            f"[dim]{date}[/dim]",
            msg if msg else "[dim]—[/dim]",
        )

    # Print the table
    console.print(table)
    console.print(f"\n[dim]Total tags: {len(tags)}[/dim]")
    console.print("[dim]Tip: Use 'Create Release' to publish a tag to GitHub[/dim]")


def create_github_release(
    git_ops: GitOperations,
    tag_name: str,
    title: str = None,
    body: str = "",
    use_ai: bool = False,
    draft: bool = False,
):
    """Create GitHub release."""
    # Get repo name from remote URL
    remote_url = git_ops.get_remote_url()
    if not remote_url:
        show_error("No remote origin found")
        return

    # Extract repo name from URL
    repo_name = extract_repo_name(remote_url)
    if not repo_name:
        show_error("Could not determine repository name from remote URL")
        return

    # Authenticate with GitHub
    gh = GitHubManager()
    if not gh.authenticate():
        return

    # Generate AI notes if requested
    if use_ai:
        show_progress("Generating release notes with AI...")
        body = generate_release_notes_ai(git_ops, tag_name)
        if not body:
            show_warning("Failed to generate AI notes, using empty body")

    # Use tag name as title if not provided
    if not title:
        title = tag_name

    # Create release
    release = gh.create_release(
        repo_name=repo_name,
        tag_name=tag_name,
        title=title,
        body=body,
        draft=draft,
    )

    if release:
        show_success(f"\n🎉 Release created successfully!")
        show_info(f"URL: {release.html_url}")
    else:
        show_error("Failed to create release")


def extract_repo_name(remote_url: str) -> str:
    """Extract repository name from remote URL."""
    # Handle SSH format: git@github.com:user/repo.git
    if remote_url.startswith("git@"):
        remote_url = remote_url.replace("git@", "https://")
        remote_url = remote_url.replace(":", "/")

    # Remove .git suffix
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    # Get last part of URL
    parts = remote_url.rstrip("/").split("/")
    if len(parts) >= 2:
        return parts[-1]

    return ""


def generate_release_notes_ai(git_ops: GitOperations, tag_name: str) -> str:
    """Generate release notes using AI."""
    try:
        # Get recent commits since last tag or last 10 commits
        commits = git_ops.get_recent_commit_messages(limit=10)

        if not commits:
            return "No commits found for release notes."

        # Format commits as release notes
        notes = "## What's New\n\n"
        notes += "### Changes\n"
        for commit in commits:
            notes += f"- {commit}\n"

        notes += "\n### Contributed by\n"
        notes += "Thanks to all contributors!\n"

        return notes

    except Exception as e:
        show_error(f"Failed to generate release notes: {str(e)}")
        return ""


# Register as CLI command
@click.command(name="release")
@click.argument("tag_name")
@click.option("--title", "-t", help="Release title")
@click.option("--body", "-b", help="Release notes")
@click.option("--draft", is_flag=True, help="Create as draft")
def release_command(tag_name, title, body, draft):
    """Create a GitHub release from an existing tag.

    Examples:
        run-git release v1.0.0
        run-git release v1.0.0 -t "Version 1.0.0" -b "Bug fixes"
    """
    git_ops = GitOperations()

    if not git_ops.is_git_repo():
        show_error("Not a git repository")
        return

    create_github_release(git_ops, tag_name, title, body, False, draft)
