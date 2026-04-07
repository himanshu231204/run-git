"""
Init command for gitpush.
"""

import os
import shutil
import tempfile
import click
from git import Repo
from git import InvalidGitRepositoryError, GitCommandError

from gitpush.core.git_operations import GitOperations
from gitpush.ui.banner import show_info, show_error, show_success, show_warning
from gitpush.ui.interactive import InteractiveUI


def is_directory_empty(path="."):
    """Check if directory is empty or only contains hidden files."""
    entries = os.listdir(path)
    # Filter out hidden files (starting with .)
    visible_entries = [f for f in entries if not f.startswith(".")]
    return len(visible_entries) == 0


def validate_repo_url(url):
    """Validate the repository URL format."""
    if not url:
        return False, "URL cannot be empty"

    url = url.strip()

    # Check for valid URL patterns
    valid_patterns = [
        "github.com",
        "gitlab.com",
        "bitbucket.org",
    ]

    url_lower = url.lower()
    is_valid = any(pattern in url_lower for pattern in valid_patterns)

    if not is_valid:
        return False, f"Invalid URL. Must be a GitHub, GitLab, or Bitbucket repository"

    # Check if URL ends with .git or is a valid clone URL (without .git suffix)
    valid_clone = (
        url.endswith(".git")
        or "github.com/" in url
        or "gitlab.com/" in url
        or "bitbucket.org/" in url
    )
    if not valid_clone:
        return False, "URL must point to a valid git repository"

    return True, url


def clone_repository(url, target_path="."):
    """
    Clone repository with proper error handling.

    Args:
        url: Repository URL to clone
        target_path: Where to clone to (default: current directory)

    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate URL first
    is_valid, result = validate_repo_url(url)
    if not is_valid:
        return False, result

    url = result

    # Check if target directory is empty
    if target_path == "." and not is_directory_empty("."):
        show_warning("Current directory is not empty!")
        show_info("Options:")
        show_info("  1. Use an empty subdirectory")
        show_info("  2. Manually remove files and try again")
        show_info("  3. Clone to a temporary location and move files")

        # Offer to clone to temp directory and move
        from gitpush.ui.interactive import InteractiveUI

        ui = InteractiveUI()

        if ui.confirm_action("Clone to temp directory and move files here?"):
            return clone_to_temp_and_move(url)

        return False, "Directory is not empty. Please use an empty directory."

    # Check if already a git repository
    try:
        Repo(target_path)
        return False, "Already a git repository. Use 'run-git pull' to update."
    except InvalidGitRepositoryError:
        pass  # Good - not a git repo

    show_info(f"Cloning from {url}...")

    try:
        Repo.clone_from(url, target_path)
        return True, "Repository cloned successfully"
    except GitCommandError as e:
        error_msg = str(e.stderr) if e.stderr else str(e)

        # Provide specific error messages for common issues
        if "authentication" in error_msg.lower() or "credential" in error_msg.lower():
            return False, "Authentication failed. Please check your credentials."
        elif "not found" in error_msg.lower() or "404" in error_msg:
            return False, "Repository not found. Please check the URL."
        elif "already exists" in error_msg.lower():
            return False, "Directory already exists. Please use an empty directory."
        else:
            return False, f"Git error: {error_msg}"
    except Exception as e:
        return False, f"Failed to clone: {str(e)}"


def clone_to_temp_and_move(url):
    """Clone to temp directory and move files to current location."""
    temp_dir = tempfile.mkdtemp(prefix="gitpush_clone_")

    try:
        show_info(f"Cloning to temporary location...")
        Repo.clone_from(url, temp_dir)

        # Move all files from temp to current directory
        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = os.path.join(".", item)
            shutil.move(src, dst)

        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

        return True, "Repository cloned successfully"
    except Exception as e:
        # Clean up on failure
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False, f"Clone failed: {str(e)}"


@click.command()
@click.argument("url", required=False)
def init_command(url):
    """Initialize git repository"""
    git_ops = GitOperations()

    if url:
        success, message = clone_repository(url, ".")

        if success:
            show_success(message)
        else:
            show_error(message)

            # Offer alternative options
            if "not empty" in message.lower():
                show_info("Tip: Create a new folder and run 'run-git init <url>' there")
    else:
        git_ops.init_repo()
        ui = InteractiveUI()
        if ui.confirm_action("Add remote repository?"):
            remote_url = ui.get_repo_url()
            git_ops.add_remote("origin", remote_url)
