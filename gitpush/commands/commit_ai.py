"""AI commit message command."""

import click

from gitpush.core.ai_engine import AIEngine
from gitpush.core.git_operations import GitOperations
from gitpush.ui.banner import show_error, show_info, show_success
from gitpush.utils.license import check_feature_access


@click.command(name="commit-ai")
def commit_ai() -> None:
    """Generate conventional commit message from git diff."""

    remaining = check_feature_access("commit-ai")
    if remaining < 0:
        return

    git_ops = GitOperations()
    if not git_ops.is_git_repo():
        show_error("Not a git repository. Run 'run-git init' first")
        return

    engine = AIEngine(git_ops=git_ops)

    try:
        message = engine.generate_commit_message()
    except Exception as exc:
        show_error(f"Failed to generate commit message: {exc}")
        return

    show_success("AI commit message generated")
    show_info("Review the message before committing:")
    click.echo(message)

    if remaining >= 0:
        show_info(f"Free uses remaining today: {remaining}")
