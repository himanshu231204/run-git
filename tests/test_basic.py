"""
Basic tests for gitpush
"""
import unittest
import tempfile
import shutil
import os
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
        shutil.rmtree(self.test_dir)
    
    def test_init_repo(self):
        """Test repository initialization"""
        self.assertFalse(self.git_ops.is_git_repo())
        self.assertTrue(self.git_ops.init_repo())
        self.assertTrue(self.git_ops.is_git_repo())
    
    def test_get_status(self):
        """Test status retrieval"""
        self.git_ops.init_repo()
        
        # Create a test file
        with open('test.txt', 'w') as f:
            f.write('test content')
        
        status = self.git_ops.get_status()
        self.assertIsNotNone(status)
        self.assertIn('test.txt', status['untracked'])
    
    def test_add_all(self):
        """Test adding files"""
        self.git_ops.init_repo()
        
        with open('test.txt', 'w') as f:
            f.write('test')
        
        self.assertTrue(self.git_ops.add_all())
    
    def test_commit(self):
        """Test committing"""
        self.git_ops.init_repo()
        
        with open('test.txt', 'w') as f:
            f.write('test')
        
        self.git_ops.add_all()
        self.assertTrue(self.git_ops.commit("Test commit"))
    
    def test_branches(self):
        """Test branch operations"""
        self.git_ops.init_repo()
        
        # Need at least one commit
        with open('test.txt', 'w') as f:
            f.write('test')
        self.git_ops.add_all()
        self.git_ops.commit("Initial commit")
        
        # Create branch
        self.assertTrue(self.git_ops.create_branch("test-branch"))
        branches = self.git_ops.get_branches()
        self.assertIn("test-branch", branches)
        
        # Switch branch
        self.assertTrue(self.git_ops.switch_branch("test-branch"))


class TestCommitGenerator(unittest.TestCase):
    """Test Commit Message Generator"""
    
    def test_categorize_files(self):
        """Test file categorization"""
        generator = CommitGenerator(None)
        
        files = ['main.py', 'test.py', 'README.md', 'config.json']
        categories = generator._categorize_files(files)
        
        self.assertGreater(categories['code'], 0)
        self.assertGreater(categories['docs'], 0)
        self.assertGreater(categories['config'], 0)


if __name__ == '__main__':
    unittest.main()
