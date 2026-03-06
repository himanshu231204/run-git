"""
Core Git operations for gitpush
"""
import os
import git
from git.exc import GitCommandError, InvalidGitRepositoryError
from gitpush.ui.banner import show_success, show_error, show_warning, show_info, show_progress


class GitOperations:
    """Handle all git operations"""
    
    def __init__(self, path="."):
        self.path = path
        self.repo = None
        self._initialize_repo()
    
    def _initialize_repo(self):
        """Initialize git repository"""
        try:
            self.repo = git.Repo(self.path)
        except InvalidGitRepositoryError:
            self.repo = None
    
    def is_git_repo(self):
        """Check if current directory is a git repository"""
        return self.repo is not None
    
    def init_repo(self, remote_url=None):
        """Initialize a new git repository"""
        try:
            if self.is_git_repo():
                show_warning("Already a git repository")
                return True
            
            show_progress("Initializing git repository...")
            self.repo = git.Repo.init(self.path)
            show_success("Git repository initialized")
            
            if remote_url:
                self.add_remote("origin", remote_url)
            
            return True
        except Exception as e:
            show_error(f"Failed to initialize repository: {str(e)}")
            return False
    
    def add_remote(self, name, url):
        """Add a remote repository"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository. Run 'gitpush init' first")
                return False
            
            # Check if remote already exists
            if name in [remote.name for remote in self.repo.remotes]:
                show_warning(f"Remote '{name}' already exists. Updating URL...")
                self.repo.delete_remote(name)
            
            show_progress(f"Adding remote '{name}'...")
            self.repo.create_remote(name, url)
            show_success(f"Remote '{name}' added successfully")
            return True
        except Exception as e:
            show_error(f"Failed to add remote: {str(e)}")
            return False
    
    def get_status(self):
        """Get repository status"""
        if not self.is_git_repo():
            return None
        
        try:
            status = {
                'untracked': self.repo.untracked_files,
                'modified': [item.a_path for item in self.repo.index.diff(None)],
                'staged': [item.a_path for item in self.repo.index.diff('HEAD')],
                'branch': self.repo.active_branch.name,
                'has_changes': len(self.repo.untracked_files) > 0 or len([item for item in self.repo.index.diff(None)]) > 0
            }
            return status
        except Exception as e:
            show_error(f"Failed to get status: {str(e)}")
            return None
    
    def add_all(self):
        """Add all changes to staging"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False
            
            show_progress("Adding all changes to staging...")
            self.repo.git.add(A=True)
            show_success("All changes added to staging")
            return True
        except Exception as e:
            show_error(f"Failed to add changes: {str(e)}")
            return False
    
    def commit(self, message):
        """Commit changes"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False
            
            show_progress(f"Committing changes...")
            self.repo.index.commit(message)
            show_success(f"Changes committed: {message}")
            return True
        except Exception as e:
            show_error(f"Failed to commit: {str(e)}")
            return False
    
    def pull(self, remote="origin", branch=None):
        """Pull changes from remote"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False
            
            if branch is None:
                branch = self.repo.active_branch.name
            
            show_progress(f"Pulling from {remote}/{branch}...")
            self.repo.git.pull(remote, branch)
            show_success(f"Successfully pulled from {remote}/{branch}")
            return True
        except GitCommandError as e:
            if "CONFLICT" in str(e):
                show_error("Merge conflict detected! Please resolve conflicts manually.")
                return False
            else:
                show_error(f"Failed to pull: {str(e)}")
                return False
        except Exception as e:
            show_error(f"Failed to pull: {str(e)}")
            return False
    
    def push(self, remote="origin", branch=None, force=False):
        """Push changes to remote"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False
            
            if branch is None:
                branch = self.repo.active_branch.name
            
            show_progress(f"Pushing to {remote}/{branch}...")
            
            if force:
                self.repo.git.push(remote, branch, force=True)
            else:
                self.repo.git.push(remote, branch)
            
            show_success(f"Successfully pushed to {remote}/{branch}")
            return True
        except GitCommandError as e:
            if "rejected" in str(e):
                show_error("Push rejected. Try pulling first or use --force (dangerous!)")
                return False
            else:
                show_error(f"Failed to push: {str(e)}")
                return False
        except Exception as e:
            show_error(f"Failed to push: {str(e)}")
            return False
    
    def get_branches(self):
        """Get list of branches"""
        try:
            if not self.is_git_repo():
                return []
            
            branches = [branch.name for branch in self.repo.branches]
            return branches
        except Exception as e:
            show_error(f"Failed to get branches: {str(e)}")
            return []
    
    def create_branch(self, branch_name):
        """Create a new branch"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False
            
            show_progress(f"Creating branch '{branch_name}'...")
            self.repo.create_head(branch_name)
            show_success(f"Branch '{branch_name}' created")
            return True
        except Exception as e:
            show_error(f"Failed to create branch: {str(e)}")
            return False
    
    def switch_branch(self, branch_name):
        """Switch to a branch"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False
            
            show_progress(f"Switching to branch '{branch_name}'...")
            self.repo.git.checkout(branch_name)
            show_success(f"Switched to branch '{branch_name}'")
            return True
        except Exception as e:
            show_error(f"Failed to switch branch: {str(e)}")
            return False
    
    def delete_branch(self, branch_name, force=False):
        """Delete a branch"""
        try:
            if not self.is_git_repo():
                show_error("Not a git repository")
                return False
            
            current_branch = self.repo.active_branch.name
            if branch_name == current_branch:
                show_error(f"Cannot delete current branch '{branch_name}'")
                return False
            
            show_progress(f"Deleting branch '{branch_name}'...")
            if force:
                self.repo.delete_head(branch_name, force=True)
            else:
                self.repo.delete_head(branch_name)
            show_success(f"Branch '{branch_name}' deleted")
            return True
        except Exception as e:
            show_error(f"Failed to delete branch: {str(e)}")
            return False
    
    def get_log(self, max_count=10):
        """Get commit log"""
        try:
            if not self.is_git_repo():
                return []
            
            commits = []
            for commit in self.repo.iter_commits(max_count=max_count):
                commits.append({
                    'hash': commit.hexsha[:7],
                    'author': commit.author.name,
                    'date': commit.committed_datetime.strftime('%Y-%m-%d %H:%M'),
                    'message': commit.message.strip()
                })
            return commits
        except Exception as e:
            show_error(f"Failed to get log: {str(e)}")
            return []
    
    def check_sensitive_files(self):
        """Check for sensitive files before commit"""
        sensitive_patterns = [
            '.env', '.env.local', '.env.production',
            'secrets.json', 'credentials.json',
            'id_rsa', 'id_dsa', '.pem',
            'password', 'secret', 'token'
        ]
        
        status = self.get_status()
        if not status:
            return []
        
        all_files = status['untracked'] + status['modified']
        sensitive_files = []
        
        for file in all_files:
            for pattern in sensitive_patterns:
                if pattern.lower() in file.lower():
                    sensitive_files.append(file)
                    break
        
        return sensitive_files
