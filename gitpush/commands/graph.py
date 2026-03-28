"""
Graph command for visualizing commit history
"""
import click
from gitpush.core.git_operations import GitOperations
from gitpush.core.graph_renderer import GraphRenderer
from gitpush.ui.banner import show_error, show_info, show_success
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


@click.command()
@click.option('--max', 'max_count', default=15, help='Maximum number of commits to show')
@click.option('--all', 'all_branches', is_flag=True, help='Show commits from all branches')
@click.option('--simple', is_flag=True, help='Simple text output')
@click.option('--graph', 'ascii_graph', is_flag=True, help='Show ASCII graph with branch lines')
@click.option('--tree', is_flag=True, help='Show branch tree view')
@click.option('-i', '--interactive', is_flag=True, help='Interactive mode - select commit to view details')
@click.option('--commit', 'commit_hash', default=None, help='Show details for specific commit')
@click.option('--diff', 'show_diff', is_flag=True, help='Show file changes in commit details')
def graph(max_count, all_branches, simple, ascii_graph, tree, interactive, commit_hash, show_diff):
    """Visualize commit history as a graph tree"""
    git_ops = GitOperations()
    
    if not git_ops.is_git_repo():
        show_error("Not a git repository. Run 'run-git init' first")
        return
    
    renderer = GraphRenderer(git_ops.repo)
    
    # Show specific commit details if requested
    if commit_hash:
        details = get_commit_details(git_ops, renderer, commit_hash, show_diff)
        if details:
            display_commit_details(details)
        else:
            show_error(f"Commit '{commit_hash}' not found")
        return
    
    if tree:
        # Show branch tree
        tree_output = renderer.get_branch_tree()
        console.print(tree_output)
        return
    
    # Get commits
    commits = renderer.get_commit_data(max_count=max_count, all_branches=all_branches)
    
    if not commits:
        show_info("No commits found")
        return
    
    # Build graph data
    graph_data = renderer.build_graph(commits)
    
    if simple:
        # Simple text output
        output = renderer.render_text_graph(graph_data, max_count=max_count)
        console.print(output)
    elif ascii_graph:
        # ASCII graph with branch lines
        output = renderer.render_ascii_graph(commits, max_count=max_count)
        console.print(output)
    elif interactive:
        # Interactive mode - let user select commit
        show_interactive_commit_details(git_ops, renderer, graph_data, show_diff)
    else:
        # Rich table output (default)
        show_rich_table(graph_data, all_branches)


def show_rich_table(graph_data, all_branches):
    """Show commits in Rich table format"""
    console.print("\n")
    
    from gitpush.ui.banner import current_theme
    title = "Commit Graph"
    if all_branches:
        title += " (All Branches)"
    
    table = Table(
        title=title,
        show_header=True,
        header_style=f"bold {current_theme.colors['primary']}",
        border_style=current_theme.colors['primary'],
        box=box.ROUNDED
    )
    
    table.add_column("#", style="dim", width=4)
    table.add_column("Hash", style="cyan", width=10)
    table.add_column("Branch", style="green", width=12)
    table.add_column("Message", style="white")
    table.add_column("Author", style="magenta", width=15)
    table.add_column("Date", style="yellow", width=12)
    
    for i, commit in enumerate(graph_data):
        # Branch indicator
        if commit['branches']:
            branch = ", ".join(commit['branches'][:2])
        else:
            branch = ""
        
        # Message (first line)
        msg = commit['message'].split('\n')[0]
        msg = msg[:40] + "..." if len(msg) > 40 else msg
        
        # Date
        date_str = commit['date'].strftime('%Y-%m-%d')
        
        # Merge indicator
        merge_prefix = "< " if commit['merge_indicator'] else ""
        
        # Hash with merge indicator
        hash_display = f"{merge_prefix}{commit['hash']}"
        
        table.add_row(
            str(i + 1),
            hash_display,
            branch,
            msg,
            commit['author'][:15],
            date_str
        )
    
    console.print(table)
    
    # Legend and hint
    console.print("\n[dim]Legend: < = merge commit | * = HEAD commit[/dim]")
    console.print("[dim]Tip: Use --graph for branch lines, -i for interactive[/dim]\n")


def show_interactive_commit_details(git_ops, renderer, graph_data, show_diff=False):
    """Show interactive commit selection and details"""
    if not graph_data:
        show_info("No commits to display")
        return
    
    while True:
        console.print("\n")
        
        # Show commit list with numbers
        panel = Panel(
            "[bold]Select a commit to view details[/bold]\n"
            "[dim]Enter the number of the commit[/dim]",
            title="[bold]Interactive Commit Viewer[/bold]",
            border_style="cyan",
            box=box.DOUBLE
        )
        console.print(panel)
        
        console.print("\n[bold]Available Commits:[/bold]\n")
        for i, commit in enumerate(graph_data):
            msg = commit['message'].split('\n')[0]
            msg = msg[:50] + "..." if len(msg) > 50 else msg
            branch = commit['branches'][0] if commit['branches'] else ""
            
            merge_tag = " [MERGE]" if commit['merge_indicator'] else ""
            console.print(f"  [{i+1}] {commit['hash']} | {branch}{merge_tag}")
            console.print(f"      {msg}\n")
        
        console.print("\n[dim]Enter number (or 'q' to quit):[/dim] ")
        
        try:
            selected = click.prompt("", type=str, default="q", show_default=False)
        except:
            break
        
        if not selected or selected.lower() == 'q':
            console.print("\n[cyan]Returning...[/cyan]\n")
            break
        
        try:
            index = int(selected) - 1
            if 0 <= index < len(graph_data):
                commit_hash = graph_data[index]['hash']
                commit_details = get_commit_details(git_ops, renderer, commit_hash, show_diff)
                
                if commit_details:
                    display_commit_details(commit_details)
            else:
                show_error("Invalid selection")
        except ValueError:
            show_error("Please enter a valid number")
        except Exception as e:
            show_error(f"Error: {str(e)}")
        
        # Ask if user wants to view more
        console.print("\n")
        try:
            more = click.confirm("View another commit?", default=True)
            if not more:
                break
        except:
            break


def get_commit_details(git_ops, renderer, commit_hash, show_diff=False):
    """Get detailed information about a commit"""
    try:
        # Get the commit object
        commit = git_ops.repo.commit(commit_hash)
        
        # Get commit stats
        try:
            parent = commit.parents[0] if commit.parents else None
            if parent:
                stat_output = git_ops.repo.git.show(commit_hash, shortstat=True)
                
                # Parse stats
                files_changed = "?"
                additions = 0
                deletions = 0
                
                parts = stat_output.split(',')
                for part in parts:
                    part = part.strip()
                    if 'file' in part:
                        files_changed = part.split()[0]
                    elif '+' in part and not '+' == part:
                        try:
                            additions = int(part.replace('+', '').strip().split()[0])
                        except:
                            pass
                    elif '-' in part and len(part) > 1:
                        try:
                            deletions = int(part.replace('-', '').strip().split()[0])
                        except:
                            pass
            else:
                files_changed = "Initial commit"
                additions = "N/A"
                deletions = "N/A"
        except:
            files_changed = "Unknown"
            additions = 0
            deletions = 0
        
        # Get diff if requested
        diff_data = None
        if show_diff and parent:
            diff_data = renderer.get_commit_diff(commit_hash)
        
        return {
            'hash': commit.hexsha,
            'short_hash': commit.hexsha[:7],
            'author': commit.author.name,
            'email': commit.author.email,
            'date': commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'message': commit.message.strip(),
            'message_short': commit.message.strip().split('\n')[0],
            'parents': [p.hexsha[:7] for p in commit.parents],
            'is_merge': len(commit.parents) > 1,
            'files_changed': files_changed,
            'additions': additions,
            'deletions': deletions,
            'diff': diff_data
        }
        
    except Exception as e:
        show_error(f"Failed to get commit details: {str(e)}")
        return None


def display_commit_details(details):
    """Display commit details in a nice format"""
    console.print("\n")
    
    # Title with hash
    title = f"Commit: {details['short_hash']}"
    if details['is_merge']:
        title += " [MERGE COMMIT]"
    
    # Build content
    content = []
    content.append(f"[bold cyan]Author:[/bold cyan]  {details['author']} <{details['email']}>")
    content.append(f"[bold cyan]Date:[/bold cyan]    {details['date']}")
    content.append("")
    content.append(f"[bold green]Message:[/bold green]")
    content.append(details['message'])
    content.append("")
    
    if details['parents']:
        content.append(f"[bold yellow]Parents:[/bold yellow]  {' '.join(details['parents'])}")
    
    content.append(f"[bold magenta]Files:[/bold magenta]  {details['files_changed']}")
    
    # Create panel
    panel = Panel(
        "\n".join(content),
        title=title,
        border_style="green",
        box=box.ROUNDED
    )
    console.print(panel)
    
    # Show commit summary
    console.print("\n[bold]Commit Summary:[/bold]")
    console.print(f"  [green]+[/green] Additions: {details['additions']}")
    console.print(f"  [red]-[/red] Deletions: {details['deletions']}")
    
    # Show file diff if available
    if details.get('diff') and details['diff'].get('files'):
        console.print("\n[bold]Changed Files:[/bold]")
        
        table = Table(
            show_header=True,
            box=box.SIMPLE
        )
        table.add_column("Status", width=8)
        table.add_column("File", style="white")
        table.add_column("+", style="green", justify="right")
        table.add_column("-", style="red", justify="right")
        
        for f in details['diff']['files']:
            status_style = "green" if f['status'] == '+' else "red" if f['status'] == '-' else "yellow"
            table.add_row(
                f"[{status_style}]{f['status']}[/{status_style}]",
                f['path'],
                f"[green]+{f['additions']}[/green]" if f['additions'] else "",
                f"[red]-{f['deletions']}[/red]" if f['deletions'] else ""
            )
        
        console.print(table)
        
        total_add = details['diff'].get('total_additions', 0)
        total_del = details['diff'].get('total_deletions', 0)
        console.print(f"\n[bold]Total:[/bold] [+{total_add}, -{total_del}]")
    
    console.print("")
