"""
Tests for tag and release functionality
"""
import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gitpush.commands.tag_release import (
    extract_repo_name,
    generate_release_notes_ai,
)
from gitpush.core.git_operations import GitOperations


class TestExtractRepoName(unittest.TestCase):
    """Test repository name extraction from URL"""

    def test_extract_https_url(self):
        """Test extracting from HTTPS URL"""
        url = "https://github.com/username/repository.git"
        result = extract_repo_name(url)
        self.assertEqual(result, "repository")

    def test_extract_https_url_no_git(self):
        """Test extracting from HTTPS URL without .git"""
        url = "https://github.com/username/repository"
        result = extract_repo_name(url)
        self.assertEqual(result, "repository")

    def test_extract_ssh_url(self):
        """Test extracting from SSH URL"""
        url = "git@github.com:username/repository.git"
        result = extract_repo_name(url)
        self.assertEqual(result, "repository")

    def test_extract_ssh_url_no_git(self):
        """Test extracting from SSH URL without .git"""
        url = "git@github.com:username/repository"
        result = extract_repo_name(url)
        self.assertEqual(result, "repository")

    def test_extract_gitlab_url(self):
        """Test extracting from GitLab URL"""
        url = "https://gitlab.com/username/repository.git"
        result = extract_repo_name(url)
        self.assertEqual(result, "repository")

    def test_extract_bitbucket_url(self):
        """Test extracting from Bitbucket URL"""
        url = "https://bitbucket.org/username/repository.git"
        result = extract_repo_name(url)
        self.assertEqual(result, "repository")

    def test_extract_invalid_url(self):
        """Test extracting from invalid URL"""
        url = "not-a-url"
        result = extract_repo_name(url)
        self.assertEqual(result, "")

    def test_extract_empty_url(self):
        """Test extracting from empty URL"""
        url = ""
        result = extract_repo_name(url)
        self.assertEqual(result, "")


class TestGenerateReleaseNotesAI(unittest.TestCase):
    """Test AI release notes generation"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_release_notes_ai(self):
        """Test generating release notes with AI"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make some commits
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("feat: add new feature")
        git_ops.commit("fix: bug fix")

        notes = generate_release_notes_ai(git_ops, "v1.0.0")

        self.assertIsInstance(notes, str)
        self.assertIn("feat", notes.lower())
        self.assertIn("fix", notes.lower())

    def test_generate_release_notes_no_commits(self):
        """Test generating release notes with no commits"""
        git_ops = GitOperations()
        git_ops.init_repo()

        notes = generate_release_notes_ai(git_ops, "v1.0.0")

        self.assertIsInstance(notes, str)
        self.assertIn("No commits", notes)


class TestGitOperationsTagFunctions(unittest.TestCase):
    """Test tag functions in GitOperations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_list_tags_returns_list(self):
        """Test list_tags returns a list"""
        git_ops = GitOperations()
        git_ops.init_repo()

        tags = git_ops.list_tags()
        self.assertIsInstance(tags, list)

    def test_list_tags_with_data(self):
        """Test list_tags returns correct data"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        # Create tag
        git_ops.create_tag("v1.0.0", message="Version 1.0.0")

        tags = git_ops.list_tags()
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0]["name"], "v1.0.0")

    def test_create_tag_lightweight(self):
        """Test creating lightweight tag"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        result = git_ops.create_tag("v1.0.0", annotated=False)
        self.assertTrue(result)

    def test_delete_tag_not_exists(self):
        """Test deleting non-existent tag"""
        git_ops = GitOperations()
        git_ops.init_repo()

        result = git_ops.delete_tag("nonexistent")
        self.assertFalse(result)


class TestTagReleaseCLI(unittest.TestCase):
    """Test CLI commands for tag/release"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_tag_command_no_repo(self):
        """Test tag command on non-repo"""
        from click.testing import CliRunner
        from gitpush.commands.tag_release import tag

        runner = CliRunner()
        result = runner.invoke(tag, ["v1.0.0"])

        self.assertIn("Not a git repository", result.output)

    def test_release_command_no_repo(self):
        """Test release command on non-repo"""
        from click.testing import CliRunner
        from gitpush.commands.tag_release import release_command

        runner = CliRunner()
        result = runner.invoke(release_command, ["v1.0.0"])

        self.assertIn("Not a git repository", result.output)

    def test_tag_command_help(self):
        """Test tag command help"""
        from click.testing import CliRunner
        from gitpush.commands.tag_release import tag

        runner = CliRunner()
        result = runner.invoke(tag, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Create and optionally release a tag", result.output)

    def test_release_command_help(self):
        """Test release command help"""
        from click.testing import CliRunner
        from gitpush.commands.tag_release import release_command

        runner = CliRunner()
        result = runner.invoke(release_command, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Create a GitHub release", result.output)


if __name__ == "__main__":
    unittest.main()
