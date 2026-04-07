"""
GitHub commands for gitpush.
"""

import os
import click
import questionary
from git import Repo
from git import InvalidGitRepositoryError, GitCommandError

from gitpush.core.github_manager import GitHubManager
from gitpush.ui.banner import show_progress, show_error, show_info, show_success, show_warning


def validate_clone_url(url):
    """Validate and clean clone URL."""
    if not url:
        return None

    url = url.strip()

    # Ensure it starts with https
    if url.startswith("git@"):
        # Convert SSH URL to HTTPS
        # e.g., git@github.com:user/repo.git -> https://github.com/user/repo.git
        url = url.replace("git@", "https://")
        url = url.replace(":", "/")

    if url.endswith(".git"):
        url = url[:-4]

    return url + ".git"


@click.command()
@click.argument("repo_name", required=True)
@click.option("--description", "-d", help="Repository description")
@click.option("--private", is_flag=True, help="Make repository private")
@click.option("--public", is_flag=True, help="Make repository public (default)")
@click.option("--gitignore", "-g", help="Gitignore template (e.g., Python, Node)")
@click.option("--license", "-l", help="License (MIT, Apache-2.0, GPL-3.0)")
@click.option("--no-readme", is_flag=True, help="Skip README creation")
@click.option("--quick", is_flag=True, help="Use smart defaults, no prompts")
def new(repo_name, description, private, public, gitignore, license, no_readme, quick):
    """Create a new GitHub repository"""
    # Validate repo name first
    repo_name = repo_name.strip()
    if not repo_name:
        show_error("Repository name cannot be empty")
        return

    gh = GitHubManager()

    if not gh.authenticate():
        return

    try:
        repo = Repo(".")
        show_error("This directory is already a git repository!")
        show_info(f"Remote: {repo.remotes.origin.url if repo.remotes else 'None'}")
        return
    except InvalidGitRepositoryError:
        pass

    config = {"name": repo_name}

    if quick:
        show_info("Using smart defaults...")
        config["description"] = description or "Created with run-git"
        config["private"] = False
        config["gitignore"] = gh.detect_language()
        config["license"] = "mit"
        config["readme"] = True
    else:
        if not description:
            description = questionary.text("Repository description:", default="").ask()
        config["description"] = description

        if not private and not public:
            visibility = questionary.select(
                "Repository visibility:", choices=["Public", "Private"]
            ).ask()
            config["private"] = visibility == "Private"
        else:
            config["private"] = private

        if not gitignore:
            detected = gh.detect_language()
            use_detected = questionary.confirm(f"Use {detected} gitignore template?").ask()
            config["gitignore"] = detected if use_detected else None
        else:
            config["gitignore"] = gitignore

        if not license:
            licenses = gh.get_license_templates()
            license_choice = questionary.select(
                "Select license:", choices=list(licenses.keys())
            ).ask()
            config["license"] = licenses[license_choice]
        else:
            config["license"] = license.lower()

        config["readme"] = not no_readme
        if not no_readme:
            config["readme"] = questionary.confirm("Create README.md?").ask()

    github_repo = gh.create_repository(config)
    if not github_repo:
        return

    # Validate and get clean clone URL
    clone_url = validate_clone_url(github_repo.clone_url)
    if not clone_url:
        show_error("Invalid repository URL received from GitHub")
        return

    html_url = github_repo.html_url.strip() if github_repo.html_url else None

    show_progress("Initializing local repository...")
    local_repo = Repo.init(".")

    if config.get("gitignore"):
        show_progress("Creating .gitignore...")
        content = gh.get_gitignore_content(config["gitignore"])
        if content:
            with open(".gitignore", "w") as f:
                f.write(content)
        else:
            show_warning("Failed to get gitignore template")

    if config.get("license"):
        show_progress("Creating LICENSE...")
        user = gh.github.get_user()
        content = gh.get_license_content(config["license"], user.name or user.login)
        if content:
            with open("LICENSE", "w") as f:
                f.write(content)
        else:
            show_warning("Failed to get license template")

    if config.get("readme"):
        show_progress("Creating README.md...")
        user = gh.github.get_user()
        content = f"# {config['name']}\n\n{config.get('description', '')}\n"
        with open("README.md", "w") as f:
            f.write(content)

    show_progress("Adding remote origin...")
    try:
        local_repo.create_remote("origin", clone_url)
    except Exception as e:
        show_error(f"Failed to add remote: {str(e)}")
        return

    show_progress("Creating initial commit...")
    try:
        local_repo.git.add(A=True)
        local_repo.index.commit("Initial commit")
        local_repo.git.branch("-M", "main")
    except Exception as e:
        show_error(f"Failed to create initial commit: {str(e)}")
        return

    show_progress("Pushing to GitHub...")
    origin = local_repo.remote("origin")

    try:
        origin.push("main")
    except GitCommandError as e:
        error_msg = str(e.stderr) if e.stderr else str(e)

        if "rejected" in error_msg.lower() or "denied" in error_msg.lower():
            show_warning("Push rejected. Attempting to sync with remote...")
            try:
                local_repo.git.pull("origin", "main", "--allow-unrelated-histories")
                origin.push("main")
                show_success("Pushed successfully after sync!")
            except Exception as sync_error:
                show_error(f"Sync failed: {str(sync_error)}")
                show_info("You can push manually with: git push -u origin main")
                return
        elif "authentication" in error_msg.lower():
            show_error("Authentication failed. Please check your GitHub credentials.")
            return
        else:
            show_error(f"Push failed: {error_msg}")
            return
    except Exception as e:
        show_error(f"Push failed: {str(e)}")
        show_info("You can push manually with: git push -u origin main")
        return

    show_success("Repository created successfully!")
    if html_url:
        show_info(f"Link: {html_url}")
