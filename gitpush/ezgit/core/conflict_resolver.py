"""
Interactive conflict resolver
"""
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from gitpush.ui.banner import show_error, show_success, show_info, show_warning

console = Console()


class ConflictResolver:
    """Handle merge conflicts interactively"""
    
    def __init__(self, repo):
        self.repo = repo
    
    def has_conflicts(self):
        """Check if there are any conflicts"""
        try:
            # Check for unmerged paths
            unmerged = self.repo.index.unmerged_blobs()
            return len(unmerged) > 0
        except:
            return False
    
    def get_conflicted_files(self):
        """Get list of conflicted files"""
        try:
            unmerged = self.repo.index.unmerged_blobs()
            return list(unmerged.keys())
        except:
            return []
    
    def show_conflict_info(self):
        """Display conflict information"""
        files = self.get_conflicted_files()
        
        if not files:
            return
        
        # Create table
        table = Table(title="⚠️  Merge Conflicts Detected", show_header=True, header_style="bold red")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="yellow")
        
        for file in files:
            table.add_row(file, "CONFLICT")
        
        console.print()
        console.print(table)
        console.print()
    
    def resolve_interactive(self):
        """Interactively resolve conflicts"""
        if not self.has_conflicts():
            show_info("No conflicts to resolve")
            return True
        
        self.show_conflict_info()
        files = self.get_conflicted_files()
        
        console.print(Panel(
            "[bold]Choose how to resolve conflicts:[/bold]\n\n"
            "1. Keep yours (local changes)\n"
            "2. Keep theirs (remote changes)\n"
            "3. Manual merge (open files in editor)\n"
            "4. Show diff\n"
            "5. Abort merge",
            title="Conflict Resolution Options",
            border_style="yellow"
        ))
        
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Keep yours (local changes)",
                "Keep theirs (remote changes)",
                "Manual merge (I'll fix it myself)",
                "Show diff",
                "Abort merge"
            ]
        ).ask()
        
        if choice == "Keep yours (local changes)":
            return self._keep_ours(files)
        elif choice == "Keep theirs (remote changes)":
            return self._keep_theirs(files)
        elif choice == "Manual merge (I'll fix it myself)":
            return self._manual_merge(files)
        elif choice == "Show diff":
            self._show_diff(files)
            return self.resolve_interactive()  # Show menu again
        elif choice == "Abort merge":
            return self._abort_merge()
        
        return False
    
    def _keep_ours(self, files):
        """Keep local changes"""
        try:
            show_info("Keeping your local changes...")
            for file in files:
                self.repo.git.checkout('--ours', file)
                self.repo.index.add([file])
            show_success("Conflicts resolved using local changes")
            return True
        except Exception as e:
            show_error(f"Failed to resolve conflicts: {str(e)}")
            return False
    
    def _keep_theirs(self, files):
        """Keep remote changes"""
        try:
            show_info("Keeping remote changes...")
            for file in files:
                self.repo.git.checkout('--theirs', file)
                self.repo.index.add([file])
            show_success("Conflicts resolved using remote changes")
            return True
        except Exception as e:
            show_error(f"Failed to resolve conflicts: {str(e)}")
            return False
    
    def _manual_merge(self, files):
        """Let user manually resolve conflicts"""
        console.print("\n[bold yellow]Opening conflicted files for manual editing...[/bold yellow]")
        console.print("\n[cyan]Files with conflicts:[/cyan]")
        for file in files:
            console.print(f"  • {file}")
        
        console.print("\n[bold]Instructions:[/bold]")
        console.print("1. Open the files listed above in your editor")
        console.print("2. Look for conflict markers: <<<<<<<, =======, >>>>>>>")
        console.print("3. Edit the files to resolve conflicts")
        console.print("4. Remove the conflict markers")
        console.print("5. Save the files")
        console.print("6. Come back here and confirm\n")
        
        confirm = questionary.confirm("Have you resolved all conflicts?").ask()
        
        if confirm:
            try:
                # Add resolved files
                for file in files:
                    self.repo.index.add([file])
                show_success("Conflicts marked as resolved")
                return True
            except Exception as e:
                show_error(f"Failed to mark conflicts as resolved: {str(e)}")
                return False
        else:
            show_warning("Conflict resolution cancelled")
            return False
    
    def _show_diff(self, files):
        """Show diff for conflicted files"""
        console.print("\n[bold cyan]Conflict Diff:[/bold cyan]\n")
        for file in files:
            try:
                console.print(f"[yellow]═══ {file} ═══[/yellow]")
                diff = self.repo.git.diff(file)
                console.print(diff)
                console.print()
            except Exception as e:
                show_error(f"Failed to show diff for {file}: {str(e)}")
    
    def _abort_merge(self):
        """Abort the merge"""
        try:
            confirm = questionary.confirm(
                "Are you sure you want to abort the merge? This will discard all changes."
            ).ask()
            
            if confirm:
                self.repo.git.merge('--abort')
                show_success("Merge aborted")
                return True
            else:
                show_info("Merge abort cancelled")
                return False
        except Exception as e:
            show_error(f"Failed to abort merge: {str(e)}")
            return False
