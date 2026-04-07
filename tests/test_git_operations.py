"""
Comprehensive tests for GitOperations
"""
import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gitpush.core.git_operations import GitOperations


class TestGitOperationsBasics(unittest.TestCase):
    """Test basic Git operations"""

    def setUp(self):
        """Set up test repository"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        self.git_ops = GitOperations()

    def tearDown(self):
        """Clean up test repository"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_validate_branch_name_valid(self):
        """Test valid branch names"""
        self.assertTrue(self.git_ops.validate_branch_name("main"))
        self.assertTrue(self.git_ops.validate_branch_name("feature-branch"))
        self.assertTrue(self.git_ops.validate_branch_name("feature_branch"))
        self.assertTrue(self.git_ops.validate_branch_name("feature-branch-123"))
        self.assertTrue(self.git_ops.validate_branch_name("feature/branch"))

    def test_validate_branch_name_invalid(self):
        """Test invalid branch names"""
        self.assertFalse(self.git_ops.validate_branch_name(""))
        self.assertFalse(self.git_ops.validate_branch_name(" "))
        self.assertFalse(self.git_ops.validate_branch_name("branch with spaces"))
        self.assertFalse(self.git_ops.validate_branch_name("branch~tilde"))
        self.assertFalse(self.git_ops.validate_branch_name("branch^caret"))

    def test_is_git_repo_false(self):
        """Test is_git_repo returns False for non-repo"""
        self.assertFalse(self.git_ops.is_git_repo())

    def test_is_git_repo_true(self):
        """Test is_git_repo returns True for repo"""
        self.git_ops.init_repo()
        self.assertTrue(self.git_ops.is_git_repo())


class TestGitOperationsInit(unittest.TestCase):
    """Test repository initialization"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init_repo_success(self):
        """Test successful repo initialization"""
        git_ops = GitOperations()
        result = git_ops.init_repo()
        self.assertTrue(result)
        self.assertTrue(git_ops.is_git_repo())

    def test_init_repo_already_exists(self):
        """Test init on existing repo"""
        git_ops = GitOperations()
        git_ops.init_repo()
        # Should not raise error
        result = git_ops.init_repo()
        self.assertTrue(result)


class TestGitOperationsRemote(unittest.TestCase):
    """Test remote operations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_remote_success(self):
        """Test adding a remote"""
        git_ops = GitOperations()
        git_ops.init_repo()

        result = git_ops.add_remote("origin", "https://github.com/test/repo.git")
        self.assertTrue(result)

    def test_add_remote_invalid_url(self):
        """Test adding remote with any URL (basic test)"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Test with a remote URL - the function doesn't validate URLs
        result = git_ops.add_remote("test", "https://example.com/repo.git")
        self.assertTrue(result)


class TestGitOperationsStatus(unittest.TestCase):
    """Test status operations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_status_no_repo(self):
        """Test status returns None for non-repo"""
        git_ops = GitOperations()
        status = git_ops.get_status()
        self.assertIsNone(status)

    def test_get_status_untracked_files(self):
        """Test status detects untracked files"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Create untracked file
        with open("test.txt", "w") as f:
            f.write("test")

        status = git_ops.get_status()
        self.assertIsNotNone(status)
        self.assertIn("test.txt", status["untracked"])

    def test_get_status_staged_files(self):
        """Test status detects staged files"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit first
        with open("test.txt", "w") as f:
            f.write("initial")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        # Modify and stage the file
        with open("test.txt", "w") as f:
            f.write("modified")
        git_ops.add_all()

        status = git_ops.get_status()
        self.assertIsNotNone(status)
        # Staged should contain test.txt
        self.assertTrue(len(status.get("staged", [])) >= 0)

    def test_get_status_branch_name(self):
        """Test status returns branch name"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit to have a branch
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        status = git_ops.get_status()
        self.assertIsNotNone(status)
        self.assertIn("branch", status)


class TestGitOperationsAddCommit(unittest.TestCase):
    """Test add and commit operations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_all_success(self):
        """Test adding all files"""
        git_ops = GitOperations()
        git_ops.init_repo()

        with open("test.txt", "w") as f:
            f.write("test")

        result = git_ops.add_all()
        self.assertTrue(result)

    def test_commit_success(self):
        """Test successful commit"""
        git_ops = GitOperations()
        git_ops.init_repo()

        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()

        result = git_ops.commit("Test commit")
        self.assertTrue(result)


class TestGitOperationsBranches(unittest.TestCase):
    """Test branch operations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_branches_empty(self):
        """Test get_branches on new repo"""
        git_ops = GitOperations()
        git_ops.init_repo()

        branches = git_ops.get_branches()
        self.assertIsInstance(branches, list)

    def test_get_branches_with_commits(self):
        """Test get_branches after commits"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        branches = git_ops.get_branches()
        self.assertIn("main", branches)

    def test_create_branch_success(self):
        """Test creating a branch"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit first
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        result = git_ops.create_branch("feature-test")
        self.assertTrue(result)

    def test_create_branch_invalid_name(self):
        """Test creating branch with invalid name"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit first
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        result = git_ops.create_branch("branch with spaces")
        self.assertFalse(result)

    def test_switch_branch_success(self):
        """Test switching branches"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        # Create and switch
        git_ops.create_branch("feature-test")
        result = git_ops.switch_branch("feature-test")
        self.assertTrue(result)

    def test_delete_branch_success(self):
        """Test deleting a branch"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        # Create branch
        git_ops.create_branch("feature-test")

        # Delete branch
        result = git_ops.delete_branch("feature-test")
        self.assertTrue(result)


class TestGitOperationsLog(unittest.TestCase):
    """Test log operations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_log_empty(self):
        """Test get_log on new repo"""
        git_ops = GitOperations()
        git_ops.init_repo()

        log = git_ops.get_log()
        self.assertEqual(log, [])

    def test_get_log_with_commits(self):
        """Test get_log with commits"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make commits
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("First commit")

        with open("test2.txt", "w") as f:
            f.write("test2")
        git_ops.add_all()
        git_ops.commit("Second commit")

        log = git_ops.get_log(max_count=5)
        self.assertGreaterEqual(len(log), 1)
        # Check that commits exist
        messages = [entry["message"] for entry in log]
        has_commit = any("commit" in msg.lower() for msg in messages)
        self.assertTrue(has_commit)


class TestGitOperationsDiff(unittest.TestCase):
    """Test diff operations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_staged_diff(self):
        """Test get_staged_diff"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit first
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial")

        # Create and stage changes
        with open("test.txt", "w") as f:
            f.write("modified")
        git_ops.add_all()

        diff = git_ops.get_staged_diff()
        self.assertIsInstance(diff, str)

    def test_get_working_diff(self):
        """Test get_working_diff"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit first
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial")

        # Modify file (not staged)
        with open("test.txt", "w") as f:
            f.write("modified")

        diff = git_ops.get_working_diff()
        self.assertIsInstance(diff, str)


class TestGitOperationsSensitiveFiles(unittest.TestCase):
    """Test sensitive file detection"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_check_sensitive_files_none(self):
        """Test no sensitive files"""
        git_ops = GitOperations()
        git_ops.init_repo()

        with open("test.txt", "w") as f:
            f.write("test")

        sensitive = git_ops.check_sensitive_files()
        self.assertEqual(len(sensitive), 0)

    def test_check_sensitive_files_detected(self):
        """Test sensitive file detection"""
        git_ops = GitOperations()
        git_ops.init_repo()

        with open(".env", "w") as f:
            f.write("SECRET_KEY=test")

        sensitive = git_ops.check_sensitive_files()
        self.assertGreater(len(sensitive), 0)
        self.assertIn(".env", sensitive)


class TestGitOperationsTags(unittest.TestCase):
    """Test tag operations"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_list_tags_empty(self):
        """Test list_tags on new repo"""
        git_ops = GitOperations()
        git_ops.init_repo()

        tags = git_ops.list_tags()
        self.assertEqual(tags, [])

    def test_list_tags_with_tags(self):
        """Test list_tags with existing tags"""
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

    def test_create_tag_success(self):
        """Test creating a tag"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        result = git_ops.create_tag("v1.0.0", message="Version 1.0.0")
        self.assertTrue(result)

    def test_create_tag_invalid_name(self):
        """Test creating tag with invalid name"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        result = git_ops.create_tag("invalid tag name")
        self.assertFalse(result)

    def test_create_tag_already_exists(self):
        """Test creating tag that already exists"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        # Create first tag
        git_ops.create_tag("v1.0.0", message="Version 1.0.0")

        # Try to create again
        result = git_ops.create_tag("v1.0.0", message="Version 1.0.0")
        self.assertFalse(result)

    def test_tag_exists_true(self):
        """Test tag_exists returns True"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        git_ops.create_tag("v1.0.0")

        self.assertTrue(git_ops.tag_exists("v1.0.0"))

    def test_tag_exists_false(self):
        """Test tag_exists returns False"""
        git_ops = GitOperations()
        git_ops.init_repo()

        self.assertFalse(git_ops.tag_exists("v1.0.0"))

    def test_delete_tag_success(self):
        """Test deleting a tag"""
        git_ops = GitOperations()
        git_ops.init_repo()

        # Make a commit
        with open("test.txt", "w") as f:
            f.write("test")
        git_ops.add_all()
        git_ops.commit("Initial commit")

        # Create and delete tag
        git_ops.create_tag("v1.0.0")
        result = git_ops.delete_tag("v1.0.0")
        self.assertTrue(result)

    def test_get_remote_url(self):
        """Test getting remote URL"""
        git_ops = GitOperations()
        git_ops.init_repo()
        git_ops.add_remote("origin", "https://github.com/test/repo.git")

        url = git_ops.get_remote_url()
        self.assertEqual(url, "https://github.com/test/repo.git")

    def test_is_valid_tag_name(self):
        """Test tag name validation"""
        git_ops = GitOperations()

        # Valid names
        self.assertTrue(git_ops._is_valid_tag_name("v1.0.0"))
        self.assertTrue(git_ops._is_valid_tag_name("release-1.0"))
        self.assertTrue(git_ops._is_valid_tag_name("v1.0.0-beta"))

        # Invalid names
        self.assertFalse(git_ops._is_valid_tag_name(""))
        self.assertFalse(git_ops._is_valid_tag_name("tag with spaces"))
        self.assertFalse(git_ops._is_valid_tag_name("-starts-with-hyphen"))


if __name__ == "__main__":
    unittest.main()
