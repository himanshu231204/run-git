"""
Comprehensive tests for gitpush
"""
import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path

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
        self.assertEqual(__version__, "1.3.0")


if __name__ == '__main__':
    unittest.main()
