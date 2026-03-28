"""
Intelligent commit message generator
"""
import os
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


class CommitGenerator:
    """Generate intelligent commit messages based on changes"""
    
    def __init__(self, repo):
        self.repo = repo
    
    def generate_message(self, custom_message=None):
        """Generate commit message"""
        if custom_message:
            return custom_message
        
        # Get changed files
        status = self._get_file_changes()
        
        if not status['added'] and not status['modified'] and not status['deleted']:
            return "chore: update files"
        
        # Generate message based on changes
        message = self._analyze_changes(status)
        return message
    
    def _get_file_changes(self):
        """Get file changes"""
        try:
            # Get staged files
            staged = [item.a_path for item in self.repo.index.diff('HEAD')]
            untracked = self.repo.untracked_files
            modified = [item.a_path for item in self.repo.index.diff(None)]
            
            # Categorize changes
            status = {
                'added': list(set(untracked)),
                'modified': list(set(modified)),
                'deleted': [],
                'all': list(set(staged + untracked + modified))
            }
            
            return status
        except Exception as e:
            logger.error(f"Failed to get file changes: {e}")
            return {'added': [], 'modified': [], 'deleted': [], 'all': []}
    
    def _analyze_changes(self, status):
        """Analyze changes and generate appropriate message"""
        added = len(status['added'])
        modified = len(status['modified'])
        deleted = len(status['deleted'])
        
        # Analyze file types
        file_types = self._categorize_files(status['all'])
        
        # Generate message prefix
        if added > 0 and modified == 0 and deleted == 0:
            prefix = "feat"
            action = "add"
        elif modified > 0 and added == 0 and deleted == 0:
            prefix = "fix"
            action = "update"
        elif deleted > 0:
            prefix = "refactor"
            action = "remove"
        else:
            prefix = "chore"
            action = "update"
        
        # Generate description
        if file_types['code'] > 0:
            category = "code"
        elif file_types['docs'] > 0:
            category = "documentation"
        elif file_types['config'] > 0:
            category = "configuration"
        elif file_types['tests'] > 0:
            category = "tests"
        else:
            category = "files"
        
        # Build final message
        message = f"{prefix}: {action} {category}"
        
        # Add details
        details = []
        if added > 0:
            details.append(f"{added} added")
        if modified > 0:
            details.append(f"{modified} modified")
        if deleted > 0:
            details.append(f"{deleted} deleted")
        
        if details:
            message += f" ({', '.join(details)})"
        
        return message
    
    def _categorize_files(self, files):
        """Categorize files by type"""
        categories = {
            'code': 0,
            'docs': 0,
            'config': 0,
            'tests': 0,
            'other': 0
        }
        
        code_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php']
        doc_extensions = ['.md', '.txt', '.rst', '.pdf', '.doc', '.docx']
        config_extensions = ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf']
        test_patterns = ['test', 'spec', '__test__']
        
        for file in files:
            file_lower = file.lower()
            ext = os.path.splitext(file)[1]
            
            # Check for tests
            if any(pattern in file_lower for pattern in test_patterns):
                categories['tests'] += 1
            # Check for code
            elif ext in code_extensions:
                categories['code'] += 1
            # Check for docs
            elif ext in doc_extensions:
                categories['docs'] += 1
            # Check for config
            elif ext in config_extensions:
                categories['config'] += 1
            else:
                categories['other'] += 1
        
        return categories
    
    def get_conventional_types(self):
        """Get list of conventional commit types"""
        return {
            'feat': 'A new feature',
            'fix': 'A bug fix',
            'docs': 'Documentation changes',
            'style': 'Code style changes (formatting, etc)',
            'refactor': 'Code refactoring',
            'test': 'Adding or updating tests',
            'chore': 'Maintenance tasks',
            'perf': 'Performance improvements',
            'ci': 'CI/CD changes',
            'build': 'Build system changes',
            'revert': 'Revert a previous commit'
        }
