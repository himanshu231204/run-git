"""
Graph rendering for visualizing commit history
"""
from collections import defaultdict
from gitpush.ui.banner import show_error


class GraphRenderer:
    """Render commit history as ASCII graph"""
    
    def __init__(self, repo):
        self.repo = repo
    
    def get_commit_data(self, max_count=50, all_branches=False):
        """Get commit data with parent information"""
        try:
            commits = []
            
            if all_branches:
                # Get all commits from all branches
                ref = self.repo.head.reference
                for commit in self.repo.iter_commits(ref, max_count=max_count):
                    commits.append(self._process_commit(commit))
            else:
                # Current branch only
                for commit in self.repo.iter_commits(max_count=max_count):
                    commits.append(self._process_commit(commit))
            
            return commits
        except Exception as e:
            show_error(f"Failed to get commit data: {str(e)}")
            return []
    
    def _process_commit(self, commit):
        """Process a single commit"""
        return {
            'hash': commit.hexsha[:7],
            'full_hash': commit.hexsha,
            'author': commit.author.name,
            'email': commit.author.email,
            'date': commit.committed_datetime,
            'message': commit.message.strip(),
            'parents': [p.hexsha[:7] for p in commit.parents],
            'is_merge': len(commit.parents) > 1
        }
    
    def build_graph(self, commits):
        """Build graph structure from commits"""
        if not commits:
            return []
        
        # Track branches by commit hash
        commit_branches = defaultdict(list)
        
        # Get branch info
        for branch in self.repo.branches:
            try:
                for commit in self.repo.iter_commits(branch, max_count=50):
                    commit_branches[commit.hexsha[:7]].append(branch.name)
            except:
                pass
        
        # Build graph lines
        graph_lines = []
        
        for i, commit in enumerate(commits):
            hash_short = commit['hash']
            branches = commit_branches.get(hash_short, [])
            
            # Determine branch indicator
            if i == 0:
                branch_indicator = "*"  # HEAD
            elif branches:
                branch_indicator = "*"
            else:
                branch_indicator = "o"
            
            # Check if merge commit
            merge_indicator = "<" if commit['is_merge'] else ""
            
            graph_lines.append({
                'hash': hash_short,
                'branch_indicator': branch_indicator,
                'merge_indicator': merge_indicator,
                'branches': branches,
                'author': commit['author'],
                'date': commit['date'],
                'message': commit['message'],
                'parents': commit['parents']
            })
        
        return graph_lines
    
    def build_ascii_graph(self, commits, max_count=30):
        """Build ASCII graph with branch lines like git log --graph"""
        if not commits:
            return []
        
        # Map commit hash to index
        hash_to_idx = {c['hash']: i for i, c in enumerate(commits)}
        
        # Track active branches per column
        # Each entry: (commit_idx, is_current_branch)
        branch_map = {}  # col_idx -> (commit_idx, branch_name)
        
        graph_lines = []
        
        for i, commit in enumerate(commits[:max_count]):
            # Build the graph line
            line_parts = []
            
            # Determine column for this commit
            col = 0
            while col in branch_map:
                col += 1
            
            # Add branch line characters
            for c in range(col):
                if c in branch_map:
                    parent_idx, _ = branch_map[c]
                    if parent_idx > i:
                        line_parts.append("|")
                    else:
                        line_parts.append(" ")
                else:
                    line_parts.append(" ")
            
            # Add commit marker
            if commit['is_merge']:
                line_parts.append("M")  # Merge commit
            else:
                line_parts.append("*")
            
            # Mark current position
            branch_map[col] = (i, commit['hash'][:4])
            
            # Add vertical lines for active branches
            # This is a simplified version - full git log --graph is complex
            for c in range(col + 1, max(col + 1, len(branch_map))):
                if c in branch_map:
                    parent_idx, _ = branch_map[c]
                    if parent_idx > i:
                        line_parts.append("|")
                    else:
                        line_parts.append(" ")
            
            # Create the graph string
            graph_str = "".join(line_parts)
            
            # Get branch name
            branch_name = ""
            if commit.get('branches'):
                branch_name = f"[{commit['branches'][0]}]"
            
            graph_lines.append({
                'graph': graph_str,
                'hash': commit['hash'],
                'branch': branch_name,
                'message': commit['message'].split('\n')[0],
                'author': commit['author'],
                'date': commit['date'],
                'is_merge': commit['is_merge']
            })
        
        return graph_lines
    
    def render_ascii_graph(self, commits, max_count=30):
        """Render as ASCII graph with branch lines"""
        if not commits:
            return "No commits found"
        
        graph_data = self.build_ascii_graph(commits, max_count)
        
        lines = []
        lines.append("")
        lines.append("=" * 70)
        lines.append("  Git Commit Graph (with branches)")
        lines.append("=" * 70 + "\n")
        
        for commit in graph_data:
            # Truncate message
            msg = commit['message'][:45]
            if len(commit['message']) > 45:
                msg += "..."
            
            # Date
            date_str = commit['date'].strftime('%Y-%m-%d %H:%M')
            
            # Merge indicator
            merge_tag = " [MERGE]" if commit['is_merge'] else ""
            
            # Build line: graph + hash + branch + message
            line = f"{commit['graph']:15} {commit['hash']} {commit['branch']:12} {msg}{merge_tag}"
            lines.append(line)
            lines.append(f"                 {date_str} | {commit['author'][:15]}")
            lines.append("")
        
        lines.append("=" * 70)
        lines.append("Legend: * = commit, M = merge commit, | = branch line")
        lines.append("")
        
        return "\n".join(lines)
    
    def render_text_graph(self, graph_data, max_count=30):
        """Render as simple text graph"""
        if not graph_data:
            return "No commits found"
        
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("  Git Commit Graph")
        lines.append("=" * 60 + "\n")
        
        for commit in graph_data[:max_count]:
            # Build branch labels
            branch_str = ""
            if commit.get('branches'):
                branch_str = f" [{', '.join(commit['branches'][:2])}]"
            
            # Date formatted
            date_str = commit['date'].strftime('%Y-%m-%d %H:%M')
            
            # Message truncated
            msg = commit['message'].split('\n')[0]
            msg = msg[:40] + "..." if len(msg) > 40 else msg
            
            # Merge indicator
            merge = " <MERGE>" if commit.get('merge_indicator') else ""
            
            # Build line
            line = f"{commit['branch_indicator']} {commit['hash']}{branch_str}{merge} | {msg}"
            lines.append(line)
            lines.append(f"  {date_str} | {commit['author'][:15]}")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append("Legend: * = commit, <MERGE> = merge, (branch) = on branch")
        lines.append("")
        
        return "\n".join(lines)
    
    def render_unicode_graph(self, commits, max_count=20):
        """Render as Unicode box drawing graph"""
        if not commits:
            return "No commits found"
        
        lines = []
        
        # Header
        lines.append("")
        lines.append("+---------------------------------------------------------------+")
        lines.append("|                   GIT COMMIT GRAPH                           |")
        lines.append("+-------------+-------------------------------------------------+")
        lines.append("| Commit      | Message                                         |")
        lines.append("+-------------+-------------------------------------------------+")
        
        for commit in commits[:max_count]:
            # Hash
            hash_part = f" {commit['hash']} "
            
            # Branch indicator
            if commit['branches']:
                branch_tag = f" [{commit['branches'][0]}]"
            else:
                branch_tag = ""
            
            # Merge indicator
            merge = " <MERGE>" if commit['merge_indicator'] else ""
            
            # Message (first line only)
            msg = commit['message'].split('\n')[0]
            msg = msg[:35] + "..." if len(msg) > 35 else msg
            
            # Build line
            msg_part = f"{msg}{branch_tag}{merge}"
            lines.append(f"|{hash_part}| {msg_part:<40} |")
            
            # Author/date on next line
            date_str = commit['date'].strftime('%Y-%m-%d %H:%M')
            lines.append(f"|             |   {date_str}  {commit['author'][:12]}")
            
            # Divider
            if commit != commits[min(max_count - 1, len(commits) - 1)]:
                lines.append("|             +-------------------------------------------------+")
        
        lines.append("+-------------+-------------------------------------------------+")
        lines.append("")
        
        return "\n".join(lines)
    
    def get_branch_tree(self):
        """Get a tree view of branches and their commits"""
        try:
            lines = []
            lines.append("\n" + "Branch Tree")
            lines.append("=" * 40)
            
            for branch in self.repo.branches:
                is_current = branch.name == self.repo.active_branch.name
                current_marker = " >>" if is_current else ""
                
                # Get last commit on this branch
                try:
                    last_commit = next(self.repo.iter_commits(branch, max_count=1))
                    last_msg = last_commit.message.strip()[:30]
                    last_hash = last_commit.hexsha[:7]
                    lines.append(f"* {branch.name}{current_marker}")
                    lines.append(f"   +-- {last_hash} - {last_msg}")
                except:
                    lines.append(f"* {branch.name}{current_marker} (empty)")
            
            lines.append("=" * 40)
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_commit_diff(self, commit_hash):
        """Get file diff for a specific commit"""
        try:
            commit = self.repo.commit(commit_hash)
            
            # Get parent
            parent = commit.parents[0] if commit.parents else None
            
            if parent:
                # Get diff with parent
                diff = parent.diff(commit)
                
                files = []
                total_additions = 0
                total_deletions = 0
                
                for d in diff:
                    # Get stats for this file
                    try:
                        old_lines = len(d.a_blob.data_stream.read().decode('utf-8', errors='ignore').splitlines()) if d.a_blob else 0
                        new_lines = len(d.b_blob.data_stream.read().decode('utf-8', errors='ignore').splitlines()) if d.b_blob else 0
                        additions = new_lines - old_lines
                    except:
                        additions = 0
                        old_lines = 0
                        new_lines = 0
                    
                    deletions = old_lines - new_lines if new_lines > 0 else 0
                    
                    status_char = self._get_status_char(d.change_type)
                    
                    files.append({
                        'path': d.a_path if d.a_path else d.b_path,
                        'status': status_char,
                        'additions': additions,
                        'deletions': deletions
                    })
                    
                    total_additions += additions
                    total_deletions += deletions
                
                return {
                    'files': files,
                    'total_additions': total_additions,
                    'total_deletions': total_deletions,
                    'files_changed': len(files)
                }
            else:
                # Initial commit - all files are new
                return {
                    'files': [],
                    'total_additions': 'N/A',
                    'total_deletions': 'N/A',
                    'files_changed': 'Initial commit',
                    'is_initial': True
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def _get_status_char(self, change_type):
        """Convert git change type to character"""
        status_map = {
            'A': '+',  # Added
            'M': 'M',  # Modified
            'D': '-',  # Deleted
            'R': 'R',  # Renamed
            'C': 'C',  # Copied
        }
        return status_map.get(change_type, '?')
    
    def get_diff_text(self, commit_hash):
        """Get actual diff text for a commit"""
        try:
            commit = self.repo.commit(commit_hash)
            parent = commit.parents[0] if commit.parents else None
            
            if parent:
                # Get diff as text
                diff_text = self.repo.git.diff(parent.hexsha, commit.hexsha, numstat=True)
                
                if not diff_text:
                    return "No changes"
                
                lines = []
                lines.append("---")
                
                for line in diff_text.split('\n'):
                    if line:
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            add = parts[0]
                            del_ = parts[1]
                            path = parts[2]
                            
                            if add == '-':
                                add = '0'
                            if del_ == '-':
                                del_ = '0'
                            
                            lines.append(f" {path}")
                            lines.append(f"   +{add} -{del_}")
                
                return '\n'.join(lines)
            else:
                # Initial commit
                diff_text = self.repo.git.show(commit.hexsha, numstat=True)
                return diff_text
                
        except Exception as e:
            return f"Error getting diff: {str(e)}"
