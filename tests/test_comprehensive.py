"""
Comprehensive tests for gitpush
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
from gitpush.core.commit_generator import CommitGenerator


class TestGitOperations(unittest.TestCase):
    """Test Git Operations"""
    
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
    
    def test_is_not_git_repo_initially(self):
        """Test that directory is not a git repo initially"""
        self.assertFalse(self.git_ops.is_git_repo())
    
    def test_init_repo(self):
        """Test repository initialization"""
        result = self.git_ops.init_repo()
        self.assertTrue(result)
        self.assertTrue(self.git_ops.is_git_repo())
    
    def test_get_status_returns_none_without_repo(self):
        """Test status returns None without repo"""
        status = self.git_ops.get_status()
        self.assertIsNone(status)
    
    def test_get_status_with_repo(self):
        """Test status with initialized repo"""
        self.git_ops.init_repo()
        
        # Create a test file
        with open('test.txt', 'w') as f:
            f.write('test content')
        
        status = self.git_ops.get_status()
        self.assertIsNotNone(status)
        self.assertIn('untracked', status)
        self.assertIn('test.txt', status['untracked'])
    
    def test_add_all(self):
        """Test adding files"""
        self.git_ops.init_repo()
        
        with open('test.txt', 'w') as f:
            f.write('test')
        
        result = self.git_ops.add_all()
        self.assertTrue(result)
    
    def test_commit(self):
        """Test committing"""
        self.git_ops.init_repo()
        
        with open('test.txt', 'w') as f:
            f.write('test')
        
        self.git_ops.add_all()
        result = self.git_ops.commit("Test commit")
        self.assertTrue(result)
    
    def test_branches(self):
        """Test branch operations"""
        self.git_ops.init_repo()
        
        # Need at least one commit
        with open('test.txt', 'w') as f:
            f.write('test')
        self.git_ops.add_all()
        self.git_ops.commit("Initial commit")
        
        # Create branch
        result = self.git_ops.create_branch("test-branch")
        self.assertTrue(result)
        
        branches = self.git_ops.get_branches()
        self.assertIn("test-branch", branches)
        
        # Switch branch
        result = self.git_ops.switch_branch("test-branch")
        self.assertTrue(result)
    
    def test_sensitive_file_detection(self):
        """Test detection of sensitive files"""
        self.git_ops.init_repo()
        
        # Create sensitive files
        with open('.env', 'w') as f:
            f.write('SECRET_KEY=test')
        
        with open('passwords.txt', 'w') as f:
            f.write('secret')
        
        sensitive_files = self.git_ops.check_sensitive_files()
        self.assertGreater(len(sensitive_files), 0)


class TestCommitGenerator(unittest.TestCase):
    """Test Commit Message Generator"""
    
    def test_categorize_python_files(self):
        """Test Python file categorization"""
        generator = CommitGenerator(None)
        
        files = ['main.py', 'app.py', 'utils.py']
        categories = generator._categorize_files(files)
        
        self.assertEqual(categories['code'], 3)
    
    def test_categorize_docs(self):
        """Test documentation file categorization"""
        generator = CommitGenerator(None)
        
        files = ['README.md', 'CONTRIBUTING.md', 'docs.txt']
        categories = generator._categorize_files(files)
        
        self.assertEqual(categories['docs'], 3)
    
    def test_categorize_config(self):
        """Test config file categorization"""
        generator = CommitGenerator(None)
        
        files = ['config.json', 'settings.yaml', 'app.toml']
        categories = generator._categorize_files(files)
        
        self.assertEqual(categories['config'], 3)
    
    def test_categorize_mixed_files(self):
        """Test mixed file categorization"""
        generator = CommitGenerator(None)
        
        files = ['main.py', 'README.md', 'config.json', 'image.png']
        categories = generator._categorize_files(files)
        
        self.assertGreater(categories['code'], 0)
        self.assertGreater(categories['docs'], 0)
        self.assertGreater(categories['config'], 0)
    
    def test_conventional_types(self):
        """Test conventional commit types"""
        generator = CommitGenerator(None)
        
        types = generator.get_conventional_types()
        self.assertIn('feat', types)
        self.assertIn('fix', types)
        self.assertIn('docs', types)
        self.assertIn('chore', types)


class TestCLI(unittest.TestCase):
    """Test CLI functionality"""
    
    def test_import_cli(self):
        """Test that CLI module can be imported"""
        try:
            from gitpush import cli
            self.assertTrue(True)
        except ImportError:
            self.fail("Failed to import CLI module")
    
    def test_version_import(self):
        """Test version import"""
        from gitpush import __version__
        self.assertIsNotNone(__version__)
        self.assertEqual(__version__, "1.4.0")


class TestGitHubManager(unittest.TestCase):
    """Test GitHub Manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_is_valid_repo_name(self):
        """Test repository name validation"""
        from gitpush.core.github_manager import GitHubManager
        
        gh = GitHubManager()
        
        # Valid names
        self.assertTrue(gh._is_valid_repo_name("my-repo"))
        self.assertTrue(gh._is_valid_repo_name("MyRepo123"))
        self.assertTrue(gh._is_valid_repo_name("repo.name"))
        
        # Invalid names
        self.assertFalse(gh._is_valid_repo_name(""))
        self.assertFalse(gh._is_valid_repo_name("-starts-with-hyphen"))
        self.assertFalse(gh._is_valid_repo_name("ends-with-hyphen-"))
    
    def test_clean_url(self):
        """Test URL cleaning"""
        from gitpush.core.github_manager import GitHubManager
        
        gh = GitHubManager()
        
        # Valid URLs
        url = gh._clean_url("https://github.com/user/repo.git")
        self.assertEqual(url, "https://github.com/user/repo.git")
        
        # URLs with whitespace
        url = gh._clean_url("  https://github.com/user/repo.git  ")
        self.assertEqual(url, "https://github.com/user/repo.git")
        
        # Invalid URLs
        self.assertIsNone(gh._clean_url(""))
        self.assertIsNone(gh._clean_url(None))
        self.assertIsNone(gh._clean_url("not-a-url"))
    
    @patch('github.Github')
    def test_repo_exists_returns_true(self, mock_github):
        """Test repo_exists returns True when repo exists"""
        from gitpush.core.github_manager import GitHubManager
        
        mock_gh_instance = MagicMock()
        mock_github.return_value = mock_gh_instance
        mock_user = MagicMock()
        mock_gh_instance.get_user.return_value = mock_user
        mock_user.get_repo.return_value = MagicMock()  # Repo found
        
        gh = GitHubManager()
        gh.github = mock_gh_instance
        
        result = gh.repo_exists("existing-repo")
        self.assertTrue(result)
    
    @patch('github.Github')
    def test_repo_exists_returns_false(self, mock_github):
        """Test repo_exists returns False when repo doesn't exist"""
        from gitpush.core.github_manager import GitHubManager
        
        mock_gh_instance = MagicMock()
        mock_github.return_value = mock_gh_instance
        mock_user = MagicMock()
        mock_gh_instance.get_user.return_value = mock_user
        mock_user.get_repo.side_effect = Exception("Not Found")
        
        gh = GitHubManager()
        gh.github = mock_gh_instance
        
        result = gh.repo_exists("nonexistent-repo")
        self.assertFalse(result)
    
    @patch('github.Github')
    def test_suggest_repo_name(self, mock_github):
        """Test repository name suggestion for existing repos"""
        from gitpush.core.github_manager import GitHubManager
        
        mock_gh_instance = MagicMock()
        mock_github.return_value = mock_gh_instance
        mock_user = MagicMock()
        mock_gh_instance.get_user.return_value = mock_user
        
        # Call sequence (starts from base-1):
        # 1. repo_exists("test-base-repo-1") - returns True (exists)
        # 2. repo_exists("test-base-repo-2") - raises Exception (doesn't exist)
        mock_user.get_repo.side_effect = [MagicMock(), Exception("Not Found")]
        
        gh = GitHubManager()
        gh.github = mock_gh_instance
        
        # Should suggest "test-base-repo-2" when "test-base-repo-1" exists
        suggested = gh.suggest_repo_name("test-base-repo")
        
        self.assertEqual(suggested, "test-base-repo-2")
    
    def test_detect_language_python(self):
        """Test language detection for Python projects"""
        from gitpush.core.github_manager import GitHubManager
        
        # Create requirements.txt
        with open('requirements.txt', 'w') as f:
            f.write("requests\n")
        
        gh = GitHubManager()
        language = gh.detect_language()
        
        self.assertEqual(language, "Python")
    
    def test_detect_language_node(self):
        """Test language detection for Node projects"""
        from gitpush.core.github_manager import GitHubManager
        
        # Create package.json
        with open('package.json', 'w') as f:
            f.write('{"name": "test"}')
        
        gh = GitHubManager()
        language = gh.detect_language()
        
        self.assertEqual(language, "Node")
    
    def test_detect_language_java(self):
        """Test language detection for Java projects"""
        from gitpush.core.github_manager import GitHubManager
        
        # Create pom.xml
        with open('pom.xml', 'w') as f:
            f.write("<project></project>")
        
        gh = GitHubManager()
        language = gh.detect_language()
        
        self.assertEqual(language, "Java")
    
    def test_detect_language_default(self):
        """Test language detection defaults to Python"""
        from gitpush.core.github_manager import GitHubManager
        
        gh = GitHubManager()
        language = gh.detect_language()
        
        self.assertEqual(language, "Python")
    
    def test_get_gitignore_templates(self):
        """Test gitignore template list"""
        from gitpush.core.github_manager import GitHubManager
        
        gh = GitHubManager()
        templates = gh.get_gitignore_templates()
        
        self.assertIn("Python", templates)
        self.assertIn("Node", templates)
        self.assertIn("Java", templates)
    
    def test_get_license_templates(self):
        """Test license template list"""
        from gitpush.core.github_manager import GitHubManager
        
        gh = GitHubManager()
        licenses = gh.get_license_templates()
        
        self.assertIn("MIT", licenses)
        self.assertIn("Apache 2.0", licenses)
        self.assertEqual(licenses["MIT"], "mit")


class TestCloneFunction(unittest.TestCase):
    """Test clone functionality"""
    
    def setUp(self):
        """Set up test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up test directory"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_is_directory_empty_true(self):
        """Test empty directory detection"""
        from gitpush.commands.init import is_directory_empty
        self.assertTrue(is_directory_empty("."))
    
    def test_is_directory_empty_false(self):
        """Test non-empty directory detection"""
        from gitpush.commands.init import is_directory_empty
        # Create a file
        with open("test.txt", "w") as f:
            f.write("test")
        self.assertFalse(is_directory_empty("."))
    
    def test_is_directory_empty_ignores_hidden(self):
        """Test that hidden files are ignored"""
        from gitpush.commands.init import is_directory_empty
        # Create hidden file
        with open(".gitignore", "w") as f:
            f.write("test")
        self.assertTrue(is_directory_empty("."))
    
    def test_validate_repo_url_empty(self):
        """Test validation of empty URL"""
        from gitpush.commands.init import validate_repo_url
        is_valid, result = validate_repo_url("")
        self.assertFalse(is_valid)
    
    def test_validate_repo_url_invalid(self):
        """Test validation of invalid URL"""
        from gitpush.commands.init import validate_repo_url
        is_valid, result = validate_repo_url("not-a-git-url")
        self.assertFalse(is_valid)
    
    def test_validate_repo_url_github(self):
        """Test validation of GitHub URL"""
        from gitpush.commands.init import validate_repo_url
        is_valid, result = validate_repo_url("https://github.com/user/repo")
        self.assertTrue(is_valid)
        self.assertEqual(result, "https://github.com/user/repo")
    
    def test_validate_repo_url_strips_whitespace(self):
        """Test that URL whitespace is stripped"""
        from gitpush.commands.init import validate_repo_url
        is_valid, result = validate_repo_url("  https://github.com/user/repo  ")
        self.assertTrue(is_valid)
        self.assertEqual(result, "https://github.com/user/repo")


if __name__ == '__main__':
    unittest.main()
