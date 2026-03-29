"""AI PR review command."""

import click

from gitpush.ai.config import AIConfig
from gitpush.core.ai_engine import AIEngine
from gitpush.core.git_operations import GitOperations
from gitpush.ui.banner import show_error, show_info, show_success
from gitpush.utils.license import check_feature_access


@click.command(name="review-ai")
@click.option("--base", "base_branch", default=None, help="Base branch for diff (default from config)")
@click.option("--head", "head_ref", default="HEAD", help="Head ref for diff (default: HEAD)")
def review_ai(base_branch: str, head_ref: str) -> None:
    """Generate AI review for a pull-request diff."""

    remaining = check_feature_access("review-ai")
    if remaining < 0:
        return

    git_ops = GitOperations()
    if not git_ops.is_git_repo():
        show_error("Not a git repository. Run 'run-git init' first")
        return

    config = AIConfig.from_env()
    resolved_base = base_branch or config.default_base_branch
    engine = AIEngine(git_ops=git_ops, config=config)

    try:
        review = engine.generate_review(base_branch=resolved_base, head_ref=head_ref)
    except Exception as exc:
        show_error(f"Failed to generate review: {exc}")
        return

    show_success("AI review generated")
    show_info(f"Diff: {resolved_base}...{head_ref}")
    click.echo(review)

    if remaining >= 0:
        show_info(f"Free uses remaining today: {remaining}")
