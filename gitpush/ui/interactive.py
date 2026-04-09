"""
Interactive UI components for gitpush
"""

import questionary
from questionary import Style as QStyle
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich import box
from rich.style import Style
from rich.rule import Rule
from gitpush.ui.banner import current_theme, show_shortcuts, show_success, show_error, show_info
from gitpush.ui.help_docs import (
    CLI_COMMANDS,
    MENU_SHORTCUTS,
    QUICK_REFERENCE,
    get_command_help,
    get_all_commands,
    get_menu_shortcuts,
    show_command_list,
    show_shortcuts_table,
    show_quick_reference,
    show_help_menu,
    show_command_details,
    show_all_shortcuts_menu,
)
from gitpush.core.git_operations import GitOperations
from gitpush.core.ai_engine import AIEngine
from gitpush.config.settings import get_settings
from gitpush.ai.config import AIConfig

console = Console()

# ══════════════════════════════════════════════════════════════════════════════
# DYNAMIC QUESTIONARY STYLES (Theme-aware)
# ══════════════════════════════════════════════════════════════════════════════

def get_menu_style(menu_type="main"):
    """Get questionary style based on current theme and menu type."""
    from gitpush.ui.banner import current_theme
    
    primary = current_theme.colors.get("primary", "cyan")
    secondary = current_theme.colors.get("secondary", "green")
    accent = current_theme.colors.get("accent", "magenta")
    warning = current_theme.colors.get("warning", "yellow")
    
    # Map Rich colors to prompt_toolkit colors
    color_map_rich_to_toolkit = {
        "cyan": "ansicyan",
        "bright_cyan": "ansicyan",
        "green": "green",
        "bright_green": "green",
        "magenta": "magenta",
        "bright_magenta": "magenta",
        "yellow": "yellow",
        "bright_yellow": "yellow",
        "blue": "blue",
        "bright_blue": "blue",
        "red": "red",
        "bright_red": "red",
        "purple": "magenta",
        "bright_cyan": "cyan",
    }
    
    # Map menu types to colors
    color_map = {
        "main": primary,
        "branch": secondary,
        "ai": accent,
        "advanced": warning,
        "settings": primary,
        "graph": primary,
        "confirm": secondary,
        "input": primary,
    }
    
    rich_color = color_map.get(menu_type, primary)
    toolkit_color = color_map_rich_to_toolkit.get(rich_color, "ansicyan")
    
    return QStyle(
        [
            ("qmark", f"fg:{toolkit_color} bold"),
            ("pointer", f"fg:{toolkit_color} bold"),
            ("highlighted", f"fg:{toolkit_color} bold"),
            ("selected", f"fg:{toolkit_color} bold"),
        ]
    )


# Legacy style references (for backward compatibility)
# These are the defaults, but will be overridden dynamically
MAIN_MENU_STYLE = QStyle(
    [
        ("qmark", "fg:ansicyan bold"),
        ("pointer", "fg:ansicyan bold"),
        ("highlighted", "fg:ansicyan bold"),
        ("selected", "fg:ansicyan bold"),
    ]
)

BRANCH_MENU_STYLE = QStyle(
    [
        ("qmark", "fg:green bold"),
        ("pointer", "fg:green bold"),
        ("highlighted", "fg:green bold"),
        ("selected", "fg:green bold"),
    ]
)

AI_MENU_STYLE = QStyle(
    [
        ("qmark", "fg:magenta bold"),
        ("pointer", "fg:magenta bold"),
        ("highlighted", "fg:magenta bold"),
        ("selected", "fg:magenta bold"),
    ]
)

ADVANCED_MENU_STYLE = QStyle(
    [
        ("qmark", "fg:yellow bold"),
        ("pointer", "fg:yellow bold"),
        ("highlighted", "fg:yellow bold"),
        ("selected", "fg:yellow bold"),
    ]
)

SETTINGS_MENU_STYLE = QStyle(
    [
        ("qmark", "fg:blue bold"),
        ("pointer", "fg:blue bold"),
        ("highlighted", "fg:blue bold"),
        ("selected", "fg:blue bold"),
    ]
)

GRAPH_MENU_STYLE = QStyle(
    [
        ("qmark", "fg:cyan bold"),
        ("pointer", "fg:cyan bold"),
        ("highlighted", "fg:cyan bold"),
        ("selected", "fg:cyan bold"),
    ]
)

CONFIRM_STYLE = QStyle(
    [
        ("qmark", "fg:green bold"),
        ("pointer", "fg:green bold"),
        ("highlighted", "fg:green bold"),
        ("selected", "fg:green bold"),
    ]
)

INPUT_STYLE = QStyle(
    [
        ("qmark", "fg:cyan bold"),
        ("pointer", "fg:cyan bold"),
        ("highlighted", "fg:cyan bold"),
        ("selected", "fg:cyan bold"),
        ("answer", "fg:cyan bold"),
        ("question", "fg:ansicyan bold"),
    ]
)


# ══════════════════════════════════════════════════════════════════════════════
# ROBUST GRID NAVIGATION SYSTEM
# ══════════════════════════════════════════════════════════════════════════════


def get_input():
    """Get a single keypress and return normalized key name.
    
    Returns:
        'UP', 'DOWN', 'LEFT', 'RIGHT', 'ENTER', 'BACK', 'QUIT'
        Single character for regular keys
        None on error
    """
    import os
    import sys
    
    if os.name == 'nt':
        # Windows: use msvcrt
        import msvcrt
        
        first = msvcrt.getch()
        
        # Check for special key prefix
        if first in (b'\x00', b'\xe0'):
            # Special key - get second byte
            second = msvcrt.getch()
            second_byte = second[0] if second else 0
            
            # Extended key codes for Windows
            if second_byte == 72:    # VK_UP
                return 'UP'
            elif second_byte == 80:  # VK_DOWN
                return 'DOWN'
            elif second_byte == 77:  # VK_RIGHT
                return 'RIGHT'
            elif second_byte == 75:  # VK_LEFT
                return 'LEFT'
            elif second_byte == 83:  # VK_DELETE
                return 'DELETE'
            elif second_byte == 71:  # VK_HOME
                return 'HOME'
            elif second_byte == 79:  # VK_END
                return 'END'
            else:
                return None
        
        # Regular key - handle common control keys
        if first == b'\r':
            return 'ENTER'
        elif first == b'\x08':
            return 'BACK'
        elif first == b'\x1b':
            return 'ESC'
        else:
            try:
                return chr(first[0]) if first else None
            except:
                return None
    
    else:
        # Unix/Linux/Mac: use tty
        import tty
        import termios
        import select
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(sys.stdin.fileno())
            
            # Read first character
            first = sys.stdin.read(1)
            
            # Check for escape sequence
            if first == '\x1b':
                # Peek for more
                if select.select([sys.stdin], [], [], 0)[0]:
                    second = sys.stdin.read(1)
                    if second == '[':
                        if select.select([sys.stdin], [], [], 0)[0]:
                            third = sys.stdin.read(1)
                            if third == 'A':
                                return 'UP'
                            elif third == 'B':
                                return 'DOWN'
                            elif third == 'C':
                                return 'RIGHT'
                            elif third == 'D':
                                return 'LEFT'
                            elif third == 'H':
                                return 'HOME'
                            elif third == 'F':
                                return 'END'
                return 'ESC'
            
            # Handle regular control keys
            if first == '\r' or first == '\n':
                return 'ENTER'
            elif first == '\x7f':  # DEL
                return 'BACK'
            else:
                return first
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def move_selection(current_index, key, total_items, columns=2):
    """Move selection based on key press with proper bounds checking.
    
    Args:
        current_index: Current selection index
        key: Normalized key name
        total_items: Total number of items
        columns: Number of columns (default 2)
    
    Returns:
        New index after move (or same if invalid move)
    """
    if key is None:
        return current_index
    
    key_lower = key.lower()
    
    # Handle special keys
    if key == 'UP' or key_lower == 'w':
        # Move up: index - columns
        new_index = current_index - columns
        return max(0, new_index)
    
    elif key == 'DOWN' or key_lower == 's':
        # Move down: index + columns
        new_index = current_index + columns
        return min(total_items - 1, new_index)
    
    elif key == 'RIGHT' or key_lower == 'd':
        # Move right: check if in left column
        row = current_index // columns
        col = current_index % columns
        
        # Can only move right if in left column (col == 0)
        if col == 0:
            # Check if right column has item at this row
            right_index = row * columns + 1
            if right_index < total_items:
                return right_index
        return current_index
    
    elif key == 'LEFT' or key_lower == 'a':
        # Move left: check if in right column
        row = current_index // columns
        col = current_index % columns
        
        # Can only move left if in right column (col == 1)
        if col == 1:
            left_index = row * columns + 0
            return left_index
        return current_index
    
    else:
        # Other keys - stay in place
        return current_index


def render_grid(options, current_index, columns=2, qmark="➜", pointer="►", clear_screen=True):
    """Render the grid menu with highlighting.
    
    Args:
        options: List of option strings
        current_index: Currently selected index
        columns: Number of columns
        qmark: Question mark character
        pointer: Selection pointer character
        clear_screen: Whether to clear screen before rendering
    """
    import os
    
    # Clear screen if requested
    if clear_screen:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print header
    print(f"\n {qmark} Select (↑↓←→ navigate, Enter select, b back):\n")
    
    # Render in pairs (left, right) for strict 2-column layout
    for i in range(0, len(options), 2):
        left_item = options[i]
        right_item = options[i + 1] if i + 1 < len(options) else ""
        
        # Determine which index is selected
        left_selected = (current_index == i)
        right_selected = (i + 1 < len(options)) and (current_index == i + 1)
        
        # Build left column with pointer if selected
        if left_selected:
            left_display = f"{pointer} {left_item}"
        else:
            left_display = f"  {left_item}"
        
        # Build right column with pointer if selected
        if right_selected:
            right_display = f"{pointer} {right_item}"
        elif right_item:
            right_display = f"  {right_item}"
        else:
            right_display = ""
        
        # Print row with proper spacing
        if right_item:
            print(f"  {left_display:<15} {right_display}")
        else:
            print(f"  {left_display}")
    
    print()


def grid_select(options, columns=2, qmark="➜", pointer="►", style=None, clear_screen=True):
    """Grid selection with FULL 2D arrow key navigation.
    
    Clean implementation with proper state management.
    
    Args:
        options: List of selectable options
        columns: Number of columns (default 2)
        qmark: Question mark prefix
        pointer: Selection pointer character
        style: (unused, for compatibility)
        clear_screen: Whether to clear screen on each render (default True)
    
    Returns:
        Selected option string, or '🔙 Back' if cancelled
    """
    if not options:
        return None
    
    # State management
    total_items = len(options)
    current_index = 0  # Start at first item
    
    # Main navigation loop
    while True:
        # Render current state
        render_grid(options, current_index, columns, qmark, pointer)
        
        # Get input
        key = get_input()
        
        if key is None:
            continue
        
        # Debug: print current state
        # print(f"[DEBUG] key={key}, index={current_index}, total={total_items}")
        
        # Handle selection keys
        if key == 'ENTER' or key == '\r' or key == '\n':
            return options[current_index]
        
        # Handle back/cancel
        if key in ['BACK', 'ESC', 'b', 'B']:
            return "🔙 Back"
        
        # Handle quit
        if key.lower() == 'q':
            return None
        
        # Move selection
        new_index = move_selection(current_index, key, total_items, columns)
        if new_index != current_index:
            current_index = new_index
            # Debug: print after movement
            # print(f"[DEBUG] moved to index={current_index}")


def refresh_menu_styles():
    """Refresh all menu styles to match current theme (call after set_theme)."""
    global MAIN_MENU_STYLE, BRANCH_MENU_STYLE, AI_MENU_STYLE
    global ADVANCED_MENU_STYLE, SETTINGS_MENU_STYLE, GRAPH_MENU_STYLE
    global CONFIRM_STYLE, INPUT_STYLE
    
    MAIN_MENU_STYLE = get_menu_style("main")
    BRANCH_MENU_STYLE = get_menu_style("branch")
    AI_MENU_STYLE = get_menu_style("ai")
    ADVANCED_MENU_STYLE = get_menu_style("advanced")
    SETTINGS_MENU_STYLE = get_menu_style("settings")
    GRAPH_MENU_STYLE = get_menu_style("graph")
    CONFIRM_STYLE = get_menu_style("confirm")
    INPUT_STYLE = get_menu_style("input")


# ══════════════════════════════════════════════════════════════════════════════
# PREMIUM MENU SYSTEM
# ══════════════════════════════════════════════════════════════════════════════


def show_repo_context():
    """Display repository context info at the top of the menu"""
    from gitpush.core.git_operations import GitOperations

    git_ops = GitOperations()

    if not git_ops.is_git_repo():
        # Show "Not a git repo" message
        panel = Panel(
            "[bold red]⚠ Not a Git Repository[/bold red]\n"
            "[dim]Run 'run-git init' to initialize or navigate to a git repo[/dim]",
            title="[bold]📁 CONTEXT[/bold]",
            border_style="red",
            box=box.ROUNDED,
        )
        console.print(panel)
        return None

    # Get repo info
    repo_name = git_ops.repo.working_dir.split("/")[-1] if git_ops.repo.working_dir else "Unknown"
    branch_name = git_ops.repo.active_branch.name if git_ops.repo.active_branch else "main"
    status_data = git_ops.get_status()

    # Calculate status
    total_changes = (
        len(status_data.get("staged", []))
        + len(status_data.get("modified", []))
        + len(status_data.get("untracked", []))
        + len(status_data.get("deleted", []))
    )

    if total_changes == 0:
        status_text = "[green]✓ Clean[/green]"
    else:
        status_text = f"[yellow]● {total_changes} change(s)[/yellow]"

    # Build context info
    context_info = (
        f"[bold cyan]Repo:[/bold cyan] {repo_name}\n"
        f"[bold green]Branch:[/bold green] {branch_name}\n"
        f"[bold magenta]Status:[/bold magenta] {status_text}"
    )

    panel = Panel(
        context_info,
        title="[bold]📁 CONTEXT[/bold]",
        border_style="cyan",
        box=box.ROUNDED,
    )
    console.print(panel)


def show_premium_menu(
    title: str,
    sections: list,
    border_color: str = "cyan",
    breadcrumb: str = "",
) -> str:
    """
    Display a premium menu with arrow key navigation.

    Args:
        title: Menu title (e.g., "RUN-GIT AI", "BRANCH OPERATIONS")
        sections: List of dicts with 'title' and 'items' keys
                 items: [(key, icon, label, description), ...]
        border_color: Color for border
        breadcrumb: Navigation breadcrumb (e.g., "Main Menu > Branch")

    Returns:
        Selected option key, "back", "quit", or empty string
    """
    # Display header panel
    panel = Panel(
        "[bold]Smart Git CLI for Developers[/bold]",
        title=f"[bold]{title}[/bold]",
        border_style=border_color,
        box=box.DOUBLE,
    )
    console.print(panel)

    # Display breadcrumb if provided
    if breadcrumb:
        console.print(f"[dim]{breadcrumb}[/dim]")

    console.print()

    # Collect all items from all sections
    all_items = []
    for section in sections:
        all_items.extend(section.get("items", []))

    # Empty state handling
    if not all_items:
        console.print("[dim]No actions available[/dim]")
        console.print()

    # Build choices for questionary (only - no static display)
    all_choices = []
    choice_map = {}

    for section in sections:
        for key, icon, label, desc in section.get("items", []):
            # Style Back option differently
            if key == "b":
                choice_text = f"{icon} {label}   →   {desc}"
            else:
                choice_text = f"{icon} {label}   →   {desc}"
            choice_map[choice_text] = key
            all_choices.append(choice_text)

    # Style map for different menus
    style_map = {
        "cyan": MAIN_MENU_STYLE,
        "green": BRANCH_MENU_STYLE,
        "magenta": AI_MENU_STYLE,
        "yellow": ADVANCED_MENU_STYLE,
        "blue": SETTINGS_MENU_STYLE,
    }

    # Use questionary with arrow key navigation
    selected = questionary.select(
        "",
        choices=all_choices,
        qmark="▶",
        pointer="►",
        style=style_map.get(border_color, MAIN_MENU_STYLE),
    ).ask()

    if selected:
        key = choice_map.get(selected, "")
        # Handle special keys
        if key == "b":
            return "back"
        elif key == "q":
            return "quit"
        return key
    return ""


class InteractiveUI:
    """Interactive terminal UI for gitpush"""

    @staticmethod
    def main_menu():
        """Show main menu and execute selected action"""
        while True:
            console.print("\n")

            # Show repository context at the top
            show_repo_context()

            # Define menu sections
            main_sections = [
                {
                    "title": "PRIMARY ACTIONS",
                    "items": [
                        ("1", "🚀", "Quick Push", "Commit + Push instantly"),
                        ("2", "🤖", "AI Assistant", "AI commit, PR, review"),
                    ],
                },
                {
                    "title": "WORKFLOW",
                    "items": [
                        ("3", "📊", "Status", "Check repo status"),
                        ("4", "🌿", "Branch", "Manage branches"),
                        ("5", "🔄", "Sync", "Pull + Push"),
                        ("6", "🌳", "Commit Graph", "Visual history"),
                    ],
                },
                {
                    "title": "SETUP & REPOS",
                    "items": [
                        ("7", "🆕", "New Repo", "Create GitHub repo"),
                        ("8", "📥", "Clone Repo", "Clone repository"),
                    ],
                },
                {
                    "title": "ADVANCED",
                    "items": [
                        ("a", "🔧", "Advanced Tools", "Stash, undo, reset"),
                        ("s", "⚙️", "Settings", "Configurations"),
                    ],
                },
                {
                    "title": "HELP",
                    "items": [
                        ("h", "📚", "Help & Docs", "Keyboard shortcuts"),
                        ("q", "❌", "Exit", "Quit application"),
                    ],
                },
            ]

            # Show premium menu and get selection
            key = show_premium_menu("🚀 RUN-GIT AI", main_sections, "cyan")

            # Map key back to choice text for logic
            choice_map = {
                "1": "Quick Push",
                "2": "AI Assistant",
                "3": "Status",
                "4": "Branch",
                "5": "Sync",
                "6": "Commit Graph",
                "7": "New Repo",
                "8": "Clone Repo",
                "a": "Advanced Tools",
                "s": "Settings",
                "h": "Help",
                "q": "Exit",
            }
            choice = choice_map.get(key, "")

            # Handle special navigation keys BEFORE choice mapping
            if key == "back":
                # In main menu, "back" just continues the loop
                continue
            elif key == "quit":
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                break

            # Handle empty choice
            if not choice:
                continue

            # Handle menu choice
            if "Exit" in choice or "Quit" in choice:
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                break

            # Execute based on selection
            if "Quick Push" in choice:
                from gitpush.commands.push import push
                from gitpush.core.git_operations import GitOperations
                from gitpush.core.commit_generator import CommitGenerator

                git_ops = GitOperations()
                if not git_ops.is_git_repo():
                    show_error("Not a git repository. Run 'run-git init' first")
                    continue

                # Show progress for add operation
                with InteractiveUI.show_operation_progress("Adding files...") as progress:
                    task = progress.add_task("Adding files...", total=None)
                    if not git_ops.add_all():
                        continue
                    progress.update(task, completed=True)

                generator = CommitGenerator(git_ops.repo)
                message = generator.generate_message()
                show_info(f"Auto-generated message: {message}")

                # Show progress for commit operation
                with InteractiveUI.show_operation_progress("Committing changes...") as progress:
                    task = progress.add_task("Committing...", total=None)
                    if not git_ops.commit(message):
                        continue
                    progress.update(task, completed=True)

                # Show progress for pull operation
                with InteractiveUI.show_operation_progress("Pulling from remote...") as progress:
                    task = progress.add_task("Pulling...", total=None)
                    git_ops.pull()
                    progress.update(task, completed=True)

                # Show progress for push operation
                with InteractiveUI.show_operation_progress("Pushing to remote...") as progress:
                    task = progress.add_task("Pushing...", total=None)
                    git_ops.push()
                    progress.update(task, completed=True)

                show_success("All operations completed successfully!")

            elif "New Repo" in choice or "new" in choice.lower():
                from gitpush.commands.github import new
                from click.testing import CliRunner

                runner = CliRunner()
                repo_name = questionary.text(
                    "Enter repository name:", qmark="➜", style=INPUT_STYLE
                ).ask()
                if repo_name:
                    result = runner.invoke(new, [repo_name, "--quick"])
                    console.print(result.output)

            elif "Clone" in choice or "clone" in choice.lower():
                from gitpush.commands.init import init_command
                from click.testing import CliRunner

                runner = CliRunner()
                url = questionary.text(
                    "Enter repository URL to clone:", qmark="➜", style=INPUT_STYLE
                ).ask()
                if url:
                    result = runner.invoke(init_command, [url])
                    console.print(result.output)

            elif "Branch" in choice:
                InteractiveUI.branch_menu()

            elif "Status" in choice:
                from gitpush.commands.status import status, log
                from gitpush.core.git_operations import GitOperations

                git_ops = GitOperations()
                status_data = git_ops.get_status()
                if status_data:
                    InteractiveUI.show_status_dashboard(status_data)
                else:
                    console.print("[yellow]No changes found[/yellow]")

                # Show log option with styled confirm
                show_log = questionary.confirm(
                    "View commit history?", qmark="➜", style=CONFIRM_STYLE
                ).ask()
                if show_log:
                    commits = git_ops.get_log(max_count=10)
                    InteractiveUI.show_log_table(commits)

            elif "Commit Graph" in choice or "Graph" in choice:
                InteractiveUI.graph_menu()

            elif "Sync" in choice:
                from gitpush.core.git_operations import GitOperations

                git_ops = GitOperations()

                with InteractiveUI.show_operation_progress("Syncing with remote...") as progress:
                    task1 = progress.add_task("Pulling changes...", total=None)
                    pull_success = git_ops.pull()
                    progress.update(task1, completed=True)

                    if pull_success:
                        task2 = progress.add_task("Pushing changes...", total=None)
                        git_ops.push()
                        progress.update(task2, completed=True)

                show_success("Sync complete!")

            elif "AI Assistant" in choice:
                InteractiveUI.ai_menu()

            elif "Settings" in choice or "Configuration" in choice:
                InteractiveUI.settings_menu()

            elif "Advanced Tools" in choice:
                InteractiveUI.advanced_menu()

            elif "Help" in choice or "Docs" in choice:
                show_help_menu()

    @staticmethod
    def branch_menu():
        """Show branch operations menu"""
        while True:
            # Define menu sections for branch operations
            branch_sections = [
                {
                    "title": "BRANCH OPERATIONS",
                    "items": [
                        ("1", "📋", "List Branches", "View all branches"),
                        ("2", "➕", "Create Branch", "Create new branch"),
                        ("3", "🔄", "Switch Branch", "Switch to branch"),
                        ("4", "🗑️", "Delete Branch", "Delete a branch"),
                        ("5", "🔀", "Merge Branch", "Merge branch"),
                        ("b", "⬅️", "Back", "Return to main menu"),
                    ],
                },
            ]

            key = show_premium_menu(
                "=== BRANCH OPERATIONS ===", branch_sections, "green", "Main Menu > Branch"
            )

            # Handle special navigation keys
            if key == "back":
                break
            elif key == "quit":
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                return

            choice_map = {
                "1": "List Branches",
                "2": "Create Branch",
                "3": "Switch Branch",
                "4": "Delete Branch",
                "5": "Merge Branch",
            }
            choice = choice_map.get(key, "")

            if not choice:
                continue

            # Initialize GitOperations with error handling
            try:
                from gitpush.core.git_operations import GitOperations

                git_ops = GitOperations()
            except Exception as e:
                show_error(f"Failed to initialize git: {e}")
                continue

            if "List" in choice:
                branches = git_ops.get_branches()
                current = git_ops.repo.active_branch.name if git_ops.is_git_repo() else "main"
                InteractiveUI.show_branches_table(branches, current)

            elif "Create" in choice:
                name = questionary.text("Enter branch name:", qmark="➜", style=INPUT_STYLE).ask()
                if name:
                    with InteractiveUI.show_operation_progress(
                        f"Creating branch '{name}'..."
                    ) as progress:
                        task = progress.add_task("Creating...", total=None)
                        git_ops.create_branch(name)
                        progress.update(task, completed=True)
                    show_success(f"Branch '{name}' created!")

            elif "Switch" in choice:
                branches = git_ops.get_branches()
                if branches:
                    selected = questionary.select(
                        "Select branch:",
                        choices=branches,
                        qmark="➜",
                        pointer="►",
                        style=BRANCH_MENU_STYLE,
                    ).ask()
                    if selected:
                        with InteractiveUI.show_operation_progress(
                            f"Switching to '{selected}'..."
                        ) as progress:
                            task = progress.add_task("Switching...", total=None)
                            git_ops.switch_branch(selected)
                            progress.update(task, completed=True)
                        show_success(f"Switched to '{selected}'!")

            elif "Delete" in choice:
                branches = git_ops.get_branches()
                if branches:
                    selected = questionary.select(
                        "Select branch to delete:",
                        choices=branches,
                        qmark="➜",
                        pointer="►",
                        style=BRANCH_MENU_STYLE,
                    ).ask()
                    if (
                        selected
                        and questionary.confirm(
                            f"Delete branch '{selected}'?", qmark="➜", style=CONFIRM_STYLE
                        ).ask()
                    ):
                        with InteractiveUI.show_operation_progress(
                            f"Deleting branch '{selected}'..."
                        ) as progress:
                            task = progress.add_task("Deleting...", total=None)
                            git_ops.delete_branch(selected)
                            progress.update(task, completed=True)
                        show_success(f"Branch '{selected}' deleted!")

            elif "Merge" in choice:
                branches = git_ops.get_branches()
                if branches:
                    selected = questionary.select(
                        "Select branch to merge:",
                        choices=branches,
                        qmark="➜",
                        pointer="►",
                        style=BRANCH_MENU_STYLE,
                    ).ask()
                    if selected:
                        try:
                            with InteractiveUI.show_operation_progress(
                                f"Merging '{selected}'..."
                            ) as progress:
                                task = progress.add_task("Merging...", total=None)
                                git_ops.repo.git.merge(selected)
                                progress.update(task, completed=True)
                            show_success(f"Merged '{selected}' successfully!")
                        except Exception as e:
                            show_error(f"Merge failed: {e}")

            # Return to submenu after action completes
            continue

    @staticmethod
    def settings_menu():
        """Show settings menu"""
        while True:
            # Define menu sections
            settings_sections = [
                {
                    "title": "SETTINGS",
                    "items": [
                        ("1", "🎨", "Theme Settings", "Change color theme"),
                        ("2", "📋", "View Config", "Show current configuration"),
                        ("b", "⬅️", "Back", "Return to main menu"),
                    ],
                },
            ]

            key = show_premium_menu(
                "=== SETTINGS ===", settings_sections, "blue", "Main Menu > Settings"
            )

            # Handle special navigation keys
            if key == "back":
                return
            elif key == "quit":
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                return

            choice_map = {
                "1": "Theme Settings",
                "2": "View Config",
            }
            choice = choice_map.get(key, "")

            if not choice:
                continue

            if "Theme" in choice:
                from gitpush.ui.banner import ThemeManager, set_theme

                theme_choice = questionary.select(
                    "Select theme:",
                    choices=["default", "dark", "light"],
                    qmark="➜",
                    pointer="►",
                    style=SETTINGS_MENU_STYLE,
                ).ask()
                if theme_choice:
                    set_theme(theme_choice)
                    show_success(f"Theme set to '{theme_choice}'!")
                continue

    @staticmethod
    def advanced_menu():
        """Show advanced tools menu"""
        while True:
            # Define menu sections
            advanced_sections = [
                {
                    "title": "ADVANCED TOOLS",
                    "items": [
                        ("1", "📦", "Stash Changes", "Temporarily save changes"),
                        ("2", "↩️", "Undo Commit", "Revert last commit"),
                        ("3", "🔗", "Remote Mgmt", "Manage remotes"),
                        ("4", "🏷️", "Tags", "List/create tags"),
                        ("5", "📜", "View Logs", "Detailed commit history"),
                        ("b", "⬅️", "Back", "Return to main menu"),
                    ],
                },
            ]

            key = show_premium_menu(
                "=== ADVANCED TOOLS ===", advanced_sections, "yellow", "Main Menu > Advanced"
            )

            # Handle special navigation keys
            if key == "back":
                return
            elif key == "quit":
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                return

            choice_map = {
                "1": "Stash Changes",
                "2": "Undo Commit",
                "3": "Remote Mgmt",
                "4": "Tags",
                "5": "View Logs",
            }
            choice = choice_map.get(key, "")

            if not choice:
                continue

            # Initialize GitOperations with error handling
            try:
                from gitpush.core.git_operations import GitOperations

                git_ops = GitOperations()
            except Exception as e:
                show_error(f"Failed to initialize git: {e}")
                continue

            if "Stash" in choice:
                try:
                    with InteractiveUI.show_operation_progress("Stashing changes...") as progress:
                        task = progress.add_task("Stashing...", total=None)
                        git_ops.repo.git.stash()
                        progress.update(task, completed=True)
                    show_success("Changes stashed!")
                except Exception as e:
                    show_error(f"Error: {e}")
                continue

            elif "Undo" in choice:
                if questionary.confirm(
                    "Undo last commit? (changes will be kept)", qmark="➜", style=CONFIRM_STYLE
                ).ask():
                    try:
                        with InteractiveUI.show_operation_progress("Undoing commit...") as progress:
                            task = progress.add_task("Undoing...", total=None)
                            git_ops.repo.git.reset("HEAD~1", soft=True)
                            progress.update(task, completed=True)
                        show_success("Last commit undone!")
                    except Exception as e:
                        show_error(f"Error: {e}")
                continue

            elif "Remote" in choice:
                InteractiveUI.show_remotes_table(git_ops)
                continue

            elif "Tags" in choice:
                from gitpush.commands.tag_release import show_tag_menu

                show_tag_menu(git_ops)
                continue

            elif "Logs" in choice:
                commits = git_ops.get_log(max_count=20)
                InteractiveUI.show_log_table(commits)
                continue

    @staticmethod
    def ai_menu():
        """Show AI assistant menu"""
        from gitpush.config.settings import get_settings

        settings = get_settings()
        current_provider = settings.get("ai_provider", "local")

        while True:
            # Define menu sections
            ai_sections = [
                {
                    "title": "AI ASSISTANT",
                    "items": [
                        ("1", "💬", "Generate Commit", "AI commit message from staged diff"),
                        ("2", "📝", "Generate PR", "AI PR description from branch diff"),
                        ("3", "🔍", "Full Review", "AI review of all changes"),
                        ("4", "📄", "Single File Review", "Review a specific file"),
                        ("5", "⚙️", "Configure Provider", "Set AI provider & API key"),
                        ("b", "⬅️", "Back", "Return to main menu"),
                    ],
                },
            ]

            key = show_premium_menu(
                "=== AI ASSISTANT ===", ai_sections, "magenta", "Main Menu > AI Assistant"
            )

            # Handle special navigation keys
            if key == "back":
                break
            elif key == "quit":
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                return

            choice_map = {
                "1": "Generate Commit",
                "2": "Generate PR",
                "3": "Full Review",
                "4": "Single File Review",
                "5": "Configure Provider",
            }
            choice = choice_map.get(key, "")

            if not choice:
                continue

            # Initialize GitOperations with error handling
            try:
                from gitpush.core.git_operations import GitOperations

                git_ops = GitOperations()
            except Exception as e:
                show_error(f"Failed to initialize git: {e}")
                continue

            if not git_ops.is_git_repo():
                show_error("Not a git repository. Run 'run-git init' first")
                continue

            if "Commit" in choice:
                try:
                    engine = AIEngine(git_ops=git_ops)
                    message = engine.generate_commit_message()
                    show_success("AI commit message generated")
                    show_info("Review the message before committing:")
                    console.print(message)
                except Exception as exc:
                    show_error(f"Failed to generate commit message: {exc}")

            elif "PR" in choice:
                # Get diff with pre-flight check
                base, head, diff = InteractiveUI._get_diff_with_check(git_ops, "PR", settings)
                if diff is None:
                    continue

                # Show diff stats and generate
                diff_lines = diff.split("\n")
                file_count = len([l for l in diff_lines if l.startswith("diff --git")])
                show_info(f"Generating PR for {file_count} files...")

                from gitpush.ai.config import AIConfig

                config = AIConfig.from_settings(settings)
                try:
                    engine = AIEngine(git_ops=git_ops, config=config)
                    description = engine.generate_pr_description(
                        base_branch=base,
                        head_ref=head,
                        commit_limit=config.default_commit_history_limit,
                    )
                    show_success("AI PR description generated")
                    show_info(f"Diff: {base}...{head}")
                    console.print(description)
                except Exception as exc:
                    show_error(f"Failed to generate PR description: {exc}")

            elif "Full Review" in choice:
                # Get diff with pre-flight check
                base, head, diff = InteractiveUI._get_diff_with_check(git_ops, "review", settings)
                if diff is None:
                    continue

                # Show diff stats and generate
                diff_lines = diff.split("\n")
                file_count = len([l for l in diff_lines if l.startswith("diff --git")])
                show_info(f"Reviewing {file_count} files...")

                from gitpush.ai.config import AIConfig

                config = AIConfig.from_settings(settings)
                try:
                    engine = AIEngine(git_ops=git_ops, config=config)
                    # Use diff directly - either from branch or from staged/working changes
                    review = engine.generate_review_from_diff(diff)
                    show_success("AI review generated")
                    show_info(
                        f"Source: {base}...{head}" if base and head else "Source: current changes"
                    )
                    # Styled output with Markdown rendering
                    review_panel = Panel(
                        Markdown(review),
                        title="📝 Code Review",
                        border_style="cyan",
                        box=box.ROUNDED,
                        padding=(1, 2),
                    )
                    console.print(review_panel)
                except Exception as exc:
                    show_error(f"Failed to generate review: {exc}")

            elif "Single File" in choice:
                # Get diff source selection (staged or branch)
                diff_source = questionary.select(
                    "Select diff source:",
                    choices=[
                        "📦 Staged Changes  - Review files you've staged",
                        "🌿 Branch Changes  - Review files between branches",
                    ],
                    qmark="➜",
                    pointer="►",
                    style=AI_MENU_STYLE,
                ).ask()

                if not diff_source:
                    continue

                diff = None
                source_info = ""

                if "Staged" in diff_source:
                    # Get staged diff
                    staged = git_ops.get_staged_diff()
                    working = git_ops.get_working_diff()
                    diff = staged if staged and staged.strip() else working
                    source_info = "staged changes"
                    if not diff or not diff.strip():
                        show_error("No staged or working changes found")
                        continue
                else:
                    # Get branch diff
                    base, head, diff = InteractiveUI._get_diff_with_check(
                        git_ops, "review", settings
                    )
                    if diff is None:
                        continue
                    source_info = f"{base}...{head}"

                # Extract list of files from diff
                files = InteractiveUI._extract_files_from_diff(diff)
                if not files:
                    show_error("No files found in diff")
                    continue

                # Let user select a file
                selected_file = questionary.select(
                    "Select file to review:",
                    choices=files,
                    qmark="➜",
                    pointer="►",
                    style=AI_MENU_STYLE,
                ).ask()

                if not selected_file:
                    continue

                # Extract diff for just that file
                file_diff = InteractiveUI._extract_file_diff(diff, selected_file)
                if not file_diff or not file_diff.strip():
                    show_error(f"Could not extract diff for {selected_file}")
                    continue

                show_info(f"Reviewing {selected_file}...")

                from gitpush.ai.config import AIConfig

                config = AIConfig.from_settings(settings)

                try:
                    engine = AIEngine(git_ops=git_ops, config=config)
                    review = engine.generate_review_from_diff(file_diff)
                    show_success(f"Review for {selected_file}")
                    show_info(f"Source: {source_info}")
                    console.print(review)
                except Exception as exc:
                    show_error(f"Failed to generate review: {exc}")

            elif "Configure Provider" in choice:
                InteractiveUI.configure_ai_provider()
                # Refresh current provider after configuration
                settings = get_settings()
                current_provider = settings.get("ai_provider", "local")

    @staticmethod
    def _get_diff_with_check(git_ops, operation_type: str, settings=None):
        """
        Helper to get diff with pre-flight check.
        Returns: (base_branch, head_ref, diff) or (None, None, None) if cancelled.
        """
        from gitpush.ai.config import AIConfig
        from gitpush.ui.banner import show_error, show_info

        if settings:
            config = AIConfig.from_settings(settings)
        else:
            config = AIConfig.from_env()

        base = questionary.text(
            "Base branch:", default=config.default_base_branch, qmark="➜", style=INPUT_STYLE
        ).ask()
        if not base:
            return None, None, None

        head = questionary.text("Head ref:", default="HEAD", qmark="➜", style=INPUT_STYLE).ask()
        if not head:
            return None, None, None

        # Check if diff exists between branches
        diff = git_ops.get_branch_diff(base_branch=base, head_ref=head)
        if not diff or not diff.strip():
            staged_diff = git_ops.get_staged_diff()
            working_diff = git_ops.get_working_diff()
            has_staged = staged_diff and staged_diff.strip()
            has_working = working_diff and working_diff.strip()

            if has_staged or has_working:
                use_fallback = questionary.confirm(
                    f"No changes between {base} and {head}. Use current changes instead?",
                    qmark="➜",
                    style=CONFIRM_STYLE,
                ).ask()
                if use_fallback:
                    diff = staged_diff if has_staged else working_diff
                    fallback_type = "PR description" if operation_type == "PR" else "review"
                    show_info(f"Using current changes for {fallback_type}")
                else:
                    return None, None, None
            else:
                show_error(f"No changes found between {base} and {head}")
                show_info("Make some changes and try again")
                return None, None, None

        return base, head, diff

    @staticmethod
    def _extract_files_from_diff(diff: str) -> list:
        """Extract list of files from diff output."""
        files = []
        for line in diff.split("\n"):
            if line.startswith("diff --git"):
                # Extract file path from: diff --git a/path/to/file b/path/to/file
                parts = line.split()
                if len(parts) >= 4:
                    # Get the "b/" version (new file)
                    file_path = parts[3].replace("b/", "")
                    files.append(file_path)
        return files

    @staticmethod
    def _extract_file_diff(full_diff: str, target_file: str) -> str:
        """Extract diff section for a specific file."""
        lines = full_diff.split("\n")
        file_diff_lines = []
        in_target_file = False

        for line in lines:
            if line.startswith("diff --git"):
                # Check if this is our target file
                in_target_file = target_file in line
            if in_target_file:
                file_diff_lines.append(line)

        return "\n".join(file_diff_lines)

    @staticmethod
    def _get_validated_api_key(provider: str) -> str:
        """
        Get and validate API key for the given provider.
        Returns API key (may be empty if user cancelled) or None if user explicitly cancelled.
        """
        import re
        from gitpush.ui.banner import show_error, show_warning, show_info

        # API key format patterns for validation (only for well-known formats)
        key_patterns = {
            "openai": r"^sk-[A-Za-z0-9-_]{20,}$",
            "anthropic": r"^sk-ant-[A-Za-z0-9-_]{20,}$",
        }

        while True:
            api_key = questionary.password(
                f"Enter {provider.upper()} API Key:", qmark="➜", style=INPUT_STYLE
            ).ask()

            # User cancelled - return None to indicate cancellation
            if api_key is None:
                return ""

            # User entered nothing - return empty string
            if not api_key:
                return ""

            # Basic format validation (only for known patterns)
            pattern = key_patterns.get(provider)
            if pattern and not re.match(pattern, api_key):
                show_warning(f"API key format may be invalid for {provider.upper()}")
                show_info("Expected format:")
                if provider == "openai":
                    show_info("  - Should start with 'sk-' followed by 20+ characters")
                elif provider == "anthropic":
                    show_info("  - Should start with 'sk-ant-' followed by 20+ characters")

                retry = questionary.confirm(
                    "Use anyway?", default=True, qmark="➜", style=CONFIRM_STYLE
                ).ask()
                if not retry:
                    continue

            return api_key

    @staticmethod
    def configure_ai_provider():
        """Configure AI provider and API key interactively"""
        from gitpush.config.settings import get_settings
        from gitpush.ui.banner import show_success, show_info

        settings = get_settings()

        # Provider options
        providers = [
            ("local", "Local (Ollama) - Free, runs locally"),
            ("openai", "OpenAI - GPT-4, GPT-4o"),
            ("anthropic", "Anthropic - Claude"),
            ("google", "Google - Gemini"),
            ("grok", "Grok - xAI"),
        ]

        # Current settings
        current_provider = settings.get("ai_provider", "local")
        current_model = settings.get(f"ai_{current_provider}_model", "")

        # Display current configuration
        panel = Panel(
            f"[bold]Current Configuration[/bold]\n"
            f"Provider: [cyan]{current_provider.upper()}[/cyan]\n"
            f"Model: [cyan]{current_model or 'default'}[/cyan]",
            title="[bold]⚙️  AI PROVIDER CONFIG[/bold]",
            border_style="yellow",
            box=box.ROUNDED,
        )
        console.print(panel)

        # Select provider
        current_provider_display = next(
            (f"{p[1]} [{p[0]}]" for p in providers if p[0] == current_provider),
            f"{providers[0][1]} [{providers[0][0]}]",
        )

        provider_choice = questionary.select(
            "Select AI Provider:",
            choices=[f"{p[1]} [{p[0]}]" for p in providers],
            default=current_provider_display,
            qmark="➜",
            pointer="►",
            style=AI_MENU_STYLE,
        ).ask()

        if not provider_choice:
            return

        # Extract provider key
        selected_provider = None
        for p in providers:
            if p[1] in provider_choice:
                selected_provider = p[0]
                break

        if not selected_provider:
            return

        # Model configuration (except for local)
        if selected_provider != "local":
            # Get current API key and model
            api_key_setting = f"ai_{selected_provider}_api_key"
            model_setting = f"ai_{selected_provider}_model"
            current_api_key = settings.get(api_key_setting, "")
            current_model = settings.get(model_setting, "")

            # Model options based on provider
            model_options = {
                "openai": [
                    "gpt-4o (recommended)",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo",
                ],
                "anthropic": [
                    "claude-3-5-sonnet-20241022 (recommended)",
                    "claude-3-5-haiku-20241022",
                    "claude-3-opus-20240229",
                ],
                "google": [
                    "gemini-1.5-pro (recommended)",
                    "gemini-1.5-flash",
                    "gemini-pro",
                ],
                "grok": [
                    "grok-2 (recommended)",
                    "grok-2-1212",
                    "grok-beta",
                ],
            }

            available_models = model_options.get(selected_provider, [])

            # Ask user to choose model or enter manually
            model_choice = questionary.select(
                "Select Model:",
                choices=available_models + ["✏️  Enter model name manually"],
                qmark="➜",
                pointer="►",
                style=AI_MENU_STYLE,
            ).ask()

            if not model_choice:
                return

            # Handle manual model entry
            if "Enter model name manually" in model_choice:
                default_model = (
                    available_models[0].split(" (")[0].strip() if available_models else ""
                )
                default_value = current_model or default_model or ""
                model_choice = questionary.text(
                    "Enter model name:", default=default_value, qmark="➜", style=INPUT_STYLE
                ).ask()
                if not model_choice:
                    return
            else:
                model_choice = model_choice.split(" (")[0].strip()

            # Ask for API key with validation
            api_key = None
            if current_api_key:
                skip_key = questionary.confirm(
                    f"API key already set for {selected_provider}. Skip or update?",
                    default=True,
                    qmark="➜",
                    style=CONFIRM_STYLE,
                ).ask()
                if not skip_key:
                    api_key = InteractiveUI._get_validated_api_key(selected_provider)
            else:
                api_key = InteractiveUI._get_validated_api_key(selected_provider)

            # Save settings
            settings.set("ai_provider", selected_provider)
            if api_key is not None:
                settings.set(api_key_setting, api_key)
            if model_choice:
                settings.set(model_setting, model_choice)
            settings.save()

            # Show confirmation with key status
            saved_key = settings.get(api_key_setting, "")
            key_status = "✓" if saved_key else "✗"
            show_success(f"AI Provider configured!")
            show_info(f"Provider: {selected_provider.upper()}")
            show_info(f"Model: {model_choice}")
            show_info(f"API Key: {key_status} {'set' if saved_key else 'NOT SET'}")
        else:
            # Local (Ollama) configuration
            local_model_setting = "ai_local_model"
            local_base_url_setting = "ai_local_base_url"
            current_local_model = settings.get(local_model_setting, "llama3.2")
            current_local_url = settings.get(
                local_base_url_setting, "http://localhost:11434/api/generate"
            )

            # Ask for model name
            model_name = questionary.text(
                "Ollama Model name:", default=current_local_model, qmark="➜", style=INPUT_STYLE
            ).ask()

            # Ask for base URL
            base_url = questionary.text(
                "Ollama Base URL:", default=current_local_url, qmark="➜", style=INPUT_STYLE
            ).ask()

            # Save settings
            settings.set("ai_provider", "local")
            if model_name:
                settings.set(local_model_setting, model_name)
            if base_url:
                settings.set(local_base_url_setting, base_url)
            settings.save()

            show_success("AI Provider configured!")
            show_info(f"Provider: LOCAL (Ollama)")
            show_info(f"Model: {model_name or current_local_model}")
            show_info(f"URL: {base_url or current_local_url}")

    @staticmethod
    def graph_menu():
        """Show graph/visualization menu"""
        while True:
            # Define menu sections
            graph_sections = [
                {
                    "title": "COMMIT GRAPH",
                    "items": [
                        ("1", "📊", "Table View", "Show commits in table format"),
                        ("2", "🌳", "ASCII Graph", "Show branch visualization"),
                        ("3", "🌿", "Branch Tree", "Show branch overview"),
                        ("4", "🔍", "View Details", "Select commit to view details"),
                        ("b", "⬅️", "Back", "Return to main menu"),
                    ],
                },
            ]

            key = show_premium_menu(
                "=== COMMIT GRAPH ===", graph_sections, "cyan", "Main Menu > Commit Graph"
            )

            # Handle special navigation keys
            if key == "back":
                break
            elif key == "quit":
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                return

            choice_map = {
                "1": "Table View",
                "2": "ASCII Graph",
                "3": "Branch Tree",
                "4": "View Details",
            }
            choice = choice_map.get(key, "")

            if not choice:
                continue

            # Initialize GitOperations with error handling
            try:
                from gitpush.core.git_operations import GitOperations
                from gitpush.core.graph_renderer import GraphRenderer

                git_ops = GitOperations()
                renderer = GraphRenderer(git_ops.repo)
            except Exception as e:
                show_error(f"Failed to initialize git: {e}")
                continue

            if "Table" in choice:
                # Show default table view
                commits = git_ops.get_log(max_count=15)
                InteractiveUI.show_log_table(commits)

            elif "ASCII" in choice or "Graph" in choice:
                from click.testing import CliRunner

                runner = CliRunner()
                result = runner.invoke(
                    __import__("gitpush.commands.graph", fromlist=["graph"]).graph,
                    ["--graph", "--max", "10"],
                )
                console.print(result.output)

            elif "Branch Tree" in choice:
                tree_output = renderer.get_branch_tree()
                console.print(tree_output)

            elif "Details" in choice:
                # Show interactive commit selection
                commits = git_ops.get_log(max_count=10)
                if commits:
                    console.print("\n[bold]Select a commit to view details:[/bold]\n")
                    for i, c in enumerate(commits):
                        console.print(f"  [{i+1}] {c['hash']} | {c['message'][:50]}")

                    selected = questionary.text(
                        "Enter commit number:", qmark="➜", style=INPUT_STYLE
                    ).ask()
                    if selected and selected.isdigit():
                        idx = int(selected) - 1
                        if 0 <= idx < len(commits):
                            commit_hash = commits[idx]["hash"]
                            # Lazy import to avoid circular import
                            from gitpush.commands.graph import (
                                get_commit_details,
                                display_commit_details,
                            )

                            details = get_commit_details(
                                git_ops, renderer, commit_hash, show_diff=True
                            )
                            if details:
                                display_commit_details(details)

    @staticmethod
    def get_commit_message():
        """Get commit message with better UI"""
        return questionary.text(
            "📝 Enter commit message (leave empty for auto-generated):",
            default="",
            qmark="➜",
            style=INPUT_STYLE,
        ).ask()

    @staticmethod
    def get_repo_url():
        """Get repository URL with validation"""
        return questionary.text(
            "🔗 Enter repository URL:",
            validate=lambda text: len(text) > 0 or "URL cannot be empty",
            qmark="➜",
            style=INPUT_STYLE,
        ).ask()

    @staticmethod
    def get_branch_name():
        """Get branch name with validation"""
        return questionary.text(
            "🌿 Enter branch name:",
            validate=lambda text: len(text) > 0 or "Branch name cannot be empty",
            qmark="➜",
            style=INPUT_STYLE,
        ).ask()

    @staticmethod
    def select_branch(branches):
        """Select a branch from list"""
        if not branches:
            console.print("[yellow]⚠️  No branches available[/yellow]")
            return None

        return questionary.select(
            "🌿 Select a branch:", choices=branches, qmark="➜", pointer="►", style=BRANCH_MENU_STYLE
        ).ask()

    @staticmethod
    def confirm_action(message):
        """Confirm an action with better styling"""
        return questionary.confirm(f"❓ {message}", qmark="➜", style=CONFIRM_STYLE).ask()

    # ══════════════════════════════════════════════════════════════════════════════
    # ENHANCED TABLE DISPLAYS WITH ZEBRA STRIPING
    # ══════════════════════════════════════════════════════════════════════════════

    @staticmethod
    def show_status_dashboard(status):
        """Display comprehensive git status dashboard with zebra-striped table"""
        # Summary panel with key stats
        untracked_count = len(status.get("untracked", []))
        modified_count = len(status.get("modified", []))
        staged_count = len(status.get("staged", []))
        deleted_count = len(status.get("deleted", []))

        # Create a summary stats row
        stats_panel = Panel(
            f"[bold cyan]Branch:[/bold cyan] {status.get('branch', 'N/A')}\n"
            f"[bold green]✓ Staged:[/bold green] {staged_count}  |  "
            f"[bold yellow]✏️  Modified:[/bold yellow] {modified_count}  |  "
            f"[bold red]🗑️  Deleted:[/bold red] {deleted_count}  |  "
            f"[bold blue]🆕 Untracked:[/bold blue] {untracked_count}",
            title="[bold]📊 REPOSITORY STATUS[/bold]",
            border_style=current_theme.colors["primary"],
            box=box.ROUNDED,
        )
        console.print(stats_panel)

        # Zebra-striped table for changes
        table = Table(
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors["primary"],
            box=box.ROUNDED,
            pad_edge=False,
            expand=True,
        )
        table.add_column("Status", style="cyan", width=12)
        table.add_column("Files", style="white", justify="left")

        # Zebra striping with alternating styles
        for idx, (category, files, icon, color) in enumerate(
            [
                ("✅ Staged", status.get("staged", []), "A", "green"),
                ("✏️  Modified", status.get("modified", []), "M", "yellow"),
                ("🗑️  Deleted", status.get("deleted", []), "D", "red"),
                ("🆕 Untracked", status.get("untracked", []), "?", "blue"),
            ]
        ):
            if files:
                # Alternating row style
                row_style = "dim" if idx % 2 == 0 else ""
                file_list = "\n".join([f"  [{color}]{icon}[/{color}]  {f}" for f in files[:10]])
                if len(files) > 10:
                    file_list += f"\n  ... and {len(files) - 10} more"
                # Only apply style tags when row_style is not empty
                if row_style:
                    table.add_row(
                        f"[{row_style}]{category}[/{row_style}]",
                        f"[{row_style}]{file_list}[/{row_style}]",
                    )
                else:
                    table.add_row(category, file_list)

        console.print(table)

        # Show detailed file lists for each category
        for category, files, icon, color in [
            ("Staged", status.get("staged", []), "A", "green"),
            ("Modified", status.get("modified", []), "M", "yellow"),
            ("Deleted", status.get("deleted", []), "D", "red"),
            ("Untracked", status.get("untracked", []), "?", "blue"),
        ]:
            if files:
                console.print(f"\n[bold {color}]📁 {category} files:[/bold {color}]")
                for f in files:
                    console.print(f"   [{color}]{icon}[/{color}]  {f}")

    @staticmethod
    def show_status_table(status):
        """Display status in enhanced table (legacy compatibility)"""
        InteractiveUI.show_status_dashboard(status)

    @staticmethod
    def show_log_table(commits):
        """Display commit log in zebra-striped table"""
        table = Table(
            title="📜 Recent Commits",
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors["primary"],
            box=box.ROUNDED,
            pad_edge=False,
        )
        table.add_column("🏷️  Hash", style=f"{current_theme.colors['warning']}", width=8)
        table.add_column("👤 Author", style=f"{current_theme.colors['primary']}", width=15)
        table.add_column("📅 Date", style=f"{current_theme.colors['success']}", width=12)
        table.add_column("💬 Message", style="white")

        for idx, commit in enumerate(commits):
            msg = commit.get("message", "")
            truncated = msg[:50] + "..." if len(msg) > 50 else msg
            # Zebra striping - alternate between dim and normal
            row_style = "dim" if idx % 2 == 0 else ""

            # Only apply style when row_style is not empty
            if row_style:
                table.add_row(
                    f"[{row_style}][yellow]{commit.get('hash', '')[:7]}[/yellow][/{row_style}]",
                    f"[{row_style}]{commit.get('author', 'Unknown')[:15]}[/{row_style}]",
                    f"[{row_style}]{commit.get('date', '')[:10]}[/{row_style}]",
                    f"[{row_style}]{truncated}[/{row_style}]",
                )
            else:
                table.add_row(
                    f"[yellow]{commit.get('hash', '')[:7]}[/yellow]",
                    commit.get("author", "Unknown")[:15],
                    commit.get("date", "")[:10],
                    truncated,
                )

        console.print()
        console.print(table)

    @staticmethod
    def show_branches_table(branches, current_branch):
        """Display branches in zebra-striped table"""
        table = Table(
            title="🌿 Branches",
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors["primary"],
            box=box.ROUNDED,
            pad_edge=False,
        )
        table.add_column("🌿 Branch", style="white")
        table.add_column("📍 Status", style=f"{current_theme.colors['success']}", justify="center")

        for idx, branch in enumerate(branches):
            is_current = branch == current_branch
            status = "✓ Current" if is_current else ""
            # Zebra striping
            row_style = "dim" if idx % 2 == 0 else ""

            if row_style:
                if is_current:
                    table.add_row(
                        f"[{row_style}][bold {current_theme.colors['success']}]► {branch}[/bold {current_theme.colors['success']}][/{row_style}]",
                        f"[{row_style}][bold {current_theme.colors['success']}]{status}[/bold {current_theme.colors['success']}][/{row_style}]",
                    )
                else:
                    table.add_row(
                        f"[{row_style}]  {branch}[/{row_style}]",
                        f"[{row_style}]{status}[/{row_style}]",
                    )
            else:
                if is_current:
                    table.add_row(
                        f"[bold {current_theme.colors['success']}]► {branch}[/bold {current_theme.colors['success']}]",
                        f"[bold {current_theme.colors['success']}]{status}[/bold {current_theme.colors['success']}]",
                    )
                else:
                    table.add_row(f"  {branch}", status)

        console.print()
        console.print(table)

    @staticmethod
    def show_remotes_table(git_ops):
        """Display remotes in a styled table"""
        remotes = list(git_ops.repo.remotes)

        if not remotes:
            show_info("No remotes configured")
            return

        table = Table(
            title="🔗 Remote Repositories",
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors["primary"],
            box=box.ROUNDED,
        )
        table.add_column("Name", style="cyan", width=15)
        table.add_column("URL", style="white")

        for idx, remote in enumerate(remotes):
            row_style = "dim" if idx % 2 == 0 else ""

            if row_style:
                table.add_row(
                    f"[{row_style}][bold cyan]{remote.name}[/bold cyan][/{row_style}]",
                    f"[{row_style}]{remote.url}[/{row_style}]",
                )
            else:
                table.add_row(
                    f"[bold cyan]{remote.name}[/bold cyan]",
                    remote.url,
                )

        console.print(table)

    @staticmethod
    def show_tags_table(git_ops):
        """Display tags in a styled table"""
        tags = list(git_ops.repo.tags)

        if not tags:
            show_info("No tags found")
            return

        table = Table(
            title="🏷️  Tags",
            show_header=True,
            header_style=f"bold {current_theme.colors['primary']}",
            border_style=current_theme.colors["primary"],
            box=box.ROUNDED,
        )
        table.add_column("Tag Name", style="yellow", width=30)
        table.add_column("Commit", style="white", width=12)

        for idx, tag in enumerate(tags):
            row_style = "dim" if idx % 2 == 0 else ""
            commit_sha = tag.commit.hexsha[:7] if hasattr(tag, "commit") else "N/A"

            if row_style:
                table.add_row(
                    f"[{row_style}][bold yellow]{tag.name}[/bold yellow][/{row_style}]",
                    f"[{row_style}]{commit_sha}[/{row_style}]",
                )
            else:
                table.add_row(
                    f"[bold yellow]{tag.name}[/bold yellow]",
                    commit_sha,
                )

        console.print(table)

    # ══════════════════════════════════════════════════════════════════════════════
    # PROGRESS BAR UTILITIES
    # ══════════════════════════════════════════════════════════════════════════════

    @staticmethod
    def show_operation_progress(description="Processing..."):
        """Create an enhanced progress bar for operations with timing"""
        progress = Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=40, complete_style="cyan", finished_style="green"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )
        progress.__enter__()
        return progress

    @staticmethod
    def show_progress_bar(description="Processing..."):
        """Create a progress bar for long operations (legacy)"""
        progress = Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            console=console,
        )
        return progress


# Command suggestions based on common mistakes
COMMAND_SUGGESTIONS = {
    "git push": "run-git push",
    "git commit": "run-git push (includes commit)",
    "git status": "run-git status",
    "git log": "run-git log",
    "git branch": "run-git branch",
    "git checkout": "run-git switch",
    "git pull": "run-git pull",
    "git clone": "run-git init",
}


def suggest_command(misspelled):
    """Suggest correct command"""
    from gitpush.ui.banner import show_suggestion

    for wrong, correct in COMMAND_SUGGESTIONS.items():
        if wrong in misspelled.lower():
            show_suggestion(correct, "is the run-git equivalent")
            return True
    return False
