"""
Documentation and Keyboard Shortcuts for run-git CLI

This module contains all CLI commands, keyboard shortcuts, and help documentation.
"""

from rich import box


def _get_menu_styles():
    """Get menu styles without creating a hard dependency on interactive UI module."""
    import questionary

    default_style = questionary.Style(
        [
            ("qmark", "fg:ansicyan bold"),
            ("pointer", "fg:ansicyan bold"),
            ("highlighted", "fg:ansicyan bold"),
            ("selected", "fg:ansicyan bold"),
            ("answer", "fg:ansicyan bold"),
        ]
    )

    try:
        from gitpush.ui.interactive import INPUT_STYLE, MAIN_MENU_STYLE

        return INPUT_STYLE, MAIN_MENU_STYLE
    except Exception:
        # Fallback keeps help/docs usable even if interactive module is mid-load.
        return default_style, default_style

# ══════════════════════════════════════════════════════════════════════════════
# CLI COMMANDS REFERENCE
# ══════════════════════════════════════════════════════════════════════════════

CLI_COMMANDS = {
    # Main Commands
    "push": {
        "name": "push",
        "description": "Quick push: add all changes, commit with auto-message, and push to remote",
        "usage": "run-git push",
        "aliases": [],
    },
    "init": {
        "name": "init",
        "description": "Initialize a new git repository or clone an existing one",
        "usage": "run-git init [directory]",
        "aliases": [],
    },
    "status": {
        "name": "status",
        "description": "Show working tree status (staged, modified, deleted files)",
        "usage": "run-git status",
        "aliases": [],
    },
    "log": {
        "name": "log",
        "description": "Show commit history",
        "usage": "run-git log [--max-count N]",
        "aliases": [],
    },
    
    # Branch Commands
    "branch": {
        "name": "branch",
        "description": "List, create, delete, or rename branches",
        "usage": "run-git branch [command] [args]",
        "aliases": ["br"],
    },
    "switch": {
        "name": "switch",
        "description": "Switch to another branch",
        "usage": "run-git switch <branch-name>",
        "aliases": ["checkout", "co"],
    },
    "merge": {
        "name": "merge",
        "description": "Merge a branch into current branch",
        "usage": "run-git merge <branch-name>",
        "aliases": [],
    },
    
    # Remote Commands
    "remote": {
        "name": "remote",
        "description": "Manage remote repositories",
        "usage": "run-git remote [command] [args]",
        "aliases": [],
    },
    "pull": {
        "name": "pull",
        "description": "Fetch and integrate changes from remote",
        "usage": "run-git pull [remote] [branch]",
        "aliases": [],
    },
    "sync": {
        "name": "sync",
        "description": "Sync with remote (pull + push)",
        "usage": "run-git sync",
        "aliases": [],
    },
    
    # Stash Commands
    "stash": {
        "name": "stash",
        "description": "Stash changes temporarily",
        "usage": "run-git stash [command] [args]",
        "aliases": [],
    },
    "undo": {
        "name": "undo",
        "description": "Undo last commit (keeps changes)",
        "usage": "run-git undo",
        "aliases": [],
    },
    
    # Repository Commands
    "new": {
        "name": "new",
        "description": "Create a new GitHub repository",
        "usage": "run-git new <repo-name> [options]",
        "aliases": [],
    },
    
    # Theme Commands
    "theme": {
        "name": "theme",
        "description": "Manage color themes (default, dark, light)",
        "usage": "run-git theme [theme-name]",
        "aliases": [],
    },
    
    # Visualization Commands
    "graph": {
        "name": "graph",
        "description": "Visualize commit history as a graph tree",
        "usage": "run-git graph [--branch <branch>] [--max N]",
        "aliases": [],
    },
    
    # AI Commands
    "commit-ai": {
        "name": "commit-ai",
        "description": "Generate conventional commit message from git diff using AI",
        "usage": "run-git commit-ai [options]",
        "aliases": ["ci"],
    },
    "pr-ai": {
        "name": "pr-ai",
        "description": "Generate structured PR description from branch diff using AI",
        "usage": "run-git pr-ai [options]",
        "aliases": ["pri"],
    },
    "review-ai": {
        "name": "review-ai",
        "description": "Generate AI review for a pull-request diff",
        "usage": "run-git review-ai [options]",
        "aliases": ["ri"],
    },
    "ai": {
        "name": "ai",
        "description": "Open interactive AI assistant menu",
        "usage": "run-git ai",
        "aliases": [],
    },
    
    # Config Commands
    "config": {
        "name": "config",
        "description": "Manage run-git configuration (API keys, settings)",
        "usage": "run-git config <command> [args]",
        "aliases": [],
    },
    
    # Tag Commands
    "tag": {
        "name": "tag",
        "description": "Create, list, or delete tags",
        "usage": "run-git tag [command] [args]",
        "aliases": [],
    },
    "release": {
        "name": "release",
        "description": "Create a GitHub release from an existing tag",
        "usage": "run-git release <tag-name> [options]",
        "aliases": [],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# KEYBOARD SHORTCUTS (Interactive Menu)
# ══════════════════════════════════════════════════════════════════════════════

MENU_SHORTCUTS = {
    "main_menu": {
        "title": "Main Menu Shortcuts",
        "items": [
            ("1", "Quick Push", "Commit and push instantly"),
            ("2", "AI Assistant", "AI commit, PR, review"),
            ("3", "Status", "Check repository status"),
            ("4", "Branch", "Manage branches"),
            ("5", "Sync", "Pull and push"),
            ("6", "Commit Graph", "Visual history"),
            ("7", "New Repo", "Create GitHub repo"),
            ("8", "Clone Repo", "Clone repository"),
            ("a", "Advanced", "Stash, undo, reset"),
            ("s", "Settings", "Configurations"),
            ("h", "Help", "Show this help"),
            ("q", "Quit", "Exit application"),
        ],
    },
    "branch_menu": {
        "title": "Branch Menu Shortcuts",
        "items": [
            ("1", "List Branches", "View all branches"),
            ("2", "Create Branch", "Create new branch"),
            ("3", "Switch Branch", "Switch to branch"),
            ("4", "Delete Branch", "Delete a branch"),
            ("5", "Merge Branch", "Merge branch"),
            ("b", "Back", "Return to main menu"),
        ],
    },
    "ai_menu": {
        "title": "AI Menu Shortcuts",
        "items": [
            ("1", "AI Commit", "Generate commit message"),
            ("2", "AI PR", "Generate PR description"),
            ("3", "AI Review", "Review changes"),
            ("4", "AI Settings", "Configure AI provider"),
            ("b", "Back", "Return to main menu"),
        ],
    },
    "advanced_menu": {
        "title": "Advanced Menu Shortcuts",
        "items": [
            ("1", "Stash Changes", "Temporarily save changes"),
            ("2", "Undo Commit", "Revert last commit"),
            ("3", "Remote Mgmt", "Manage remotes"),
            ("4", "Tags", "List/create tags"),
            ("5", "View Logs", "Detailed commit history"),
            ("b", "Back", "Return to main menu"),
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# NAVIGATION KEYS
# ══════════════════════════════════════════════════════════════════════════════

NAVIGATION_KEYS = {
    "arrow_keys": "Navigate menu options",
    "enter": "Select current option",
    "escape": "Cancel/go back",
    "ctrl_c": "Exit application",
}


# ══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ══════════════════════════════════════════════════════════════════════════════

QUICK_REFERENCE = """
╭─────────────────────────────────────────────────────────────────────────────────╮
│                           RUN-GIT CLI QUICK REFERENCE                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│  QUICK START                                                                   │
│  ───────────                                                                   │
│  run-git              Start interactive menu                                    │
│  run-git push        Quick add + commit + push                                │
│  run-git status      Check repository status                                  │
│  run-git ai          Open AI assistant                                         │
│                                                                                 │
│  BRANCH OPERATIONS                                                              │
│  ─────────────────                                                             │
│  run-git branch              List branches                                    │
│  run-git switch <branch>    Switch to branch                                  │
│  run-git merge <branch>     Merge branch                                      │
│                                                                                 │
│  REMOTE OPERATIONS                                                             │
│  ───────────────                                                               │
│  run-git pull          Pull changes                                            │
│  run-git push          Push changes                                            │
│  run-git sync          Pull + Push                                             │
│  run-git remote -v     List remotes                                           │
│                                                                                 │
│  AI FEATURES                                                                  │
│  ───────────                                                                   │
│  run-git commit-ai     AI generate commit message                              │
│  run-git pr-ai         AI generate PR description                             │
│  run-git review-ai     AI review changes                                       │
│  run-git ai            Interactive AI menu                                     │
│                                                                                 │
│  CONFIGURATION                                                                 │
│  ─────────────                                                                  │
│  run-git theme         Show available themes                                   │
│  run-git theme dark    Switch to dark theme                                    │
│  run-git config status Show license and config                                 │
│                                                                                 │
│  OPTIONS                                                                       │
│  ────────                                                                       │
│  -v, --version      Show version                                                │
│  -h, --help         Show help                                                  │
╰─────────────────────────────────────────────────────────────────────────────────╯
"""


# ══════════════════════════════════════════════════════════════════════════════
# HELP FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_command_help(command_name):
    """Get help text for a specific command."""
    return CLI_COMMANDS.get(command_name, None)


def get_all_commands():
    """Get list of all available commands."""
    return list(CLI_COMMANDS.keys())


def get_menu_shortcuts(menu_type="main_menu"):
    """Get keyboard shortcuts for a specific menu."""
    return MENU_SHORTCUTS.get(menu_type, MENU_SHORTCUTS["main_menu"])


def show_command_list():
    """Display all available commands - simple text version for Windows compatibility."""
    print("\n" + "=" * 60)
    print(" CLI COMMANDS".center(60))
    print("=" * 60)
    print()
    
    for cmd, info in CLI_COMMANDS.items():
        # Format nicely
        desc = info["description"][:40] if len(info["description"]) > 40 else info["description"]
        usage = info["usage"]
        print(f"  {cmd:<15} {desc}")
        print(f"  {' '*15} {usage}")
        print()
    
    print("=" * 60)


def show_shortcuts_table(menu_type="main_menu"):
    """Display keyboard shortcuts for a menu."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from gitpush.ui.banner import current_theme
    
    console = Console()
    primary = current_theme.colors.get("primary", "cyan")
    
    shortcuts = get_menu_shortcuts(menu_type)
    
    # Compact table
    table = Table(
        show_header=True,
        header_style=f"bold {primary}",
        box=box.SIMPLE,
        pad_edge=False,
    )
    
    table.add_column("Key", style=f"bold {primary}", width=6, justify="center")
    table.add_column("Action", style="white", width=22)
    table.add_column("Description", style="dim")
    
    for key, action, description in shortcuts["items"]:
        table.add_row(key, action, description)
    
    # Compact header
    header = Panel(
        f"[bold {primary}]{shortcuts['title']}[/bold {primary}]",
        border_style=primary,
        box=box.SIMPLE,
        padding=(0, 1),
    )
    console.print(header)
    console.print(table)
    console.print()


def show_quick_reference():
    """Display quick reference guide."""
    from rich.console import Console
    from rich.text import Text
    
    console = Console()
    console.print(QUICK_REFERENCE)


def show_help_menu():
    """Show interactive help menu with all commands."""
    import questionary
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from gitpush.ui.banner import current_theme
    INPUT_STYLE, MAIN_MENU_STYLE = _get_menu_styles()
    
    console = Console()
    primary = current_theme.colors.get("primary", "cyan")
    
    while True:
        # Build choices for help topics
        help_choices = [
            "📋 All Commands List",
            "⌨️  Keyboard Shortcuts",
            "⚡ Quick Reference",
            "🔙 Back to Main Menu",
        ]
        
        console.print("\n")
        panel = Panel(
            "Choose a help topic:",
            title="Help & Docs",
            border_style=primary,
            box=box.ROUNDED,
        )
        console.print(panel)
        
        choice = questionary.select(
            "",
            choices=help_choices,
            qmark="➜",
            pointer="►",
            style=MAIN_MENU_STYLE,
        ).ask()
        
        if not choice:
            break
        
        if "All Commands" in choice:
            while True:
                command_names = list(CLI_COMMANDS.keys())
                detail_choice = questionary.select(
                    "Select a command to view details:",
                    choices=command_names + ["🔙 Back"],
                    qmark="➜",
                    pointer="►",
                    style=INPUT_STYLE,
                ).ask()

                if not detail_choice or detail_choice == "🔙 Back":
                    break

                show_command_details(detail_choice)
        
        elif "Keyboard Shortcuts" in choice:
            show_all_shortcuts_menu()
        
        elif "Quick Reference" in choice:
            show_quick_reference()
        
        elif "Back" in choice:
            break


def show_command_details(command_name):
    """Show detailed help for a specific command."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from gitpush.ui.banner import current_theme
    
    console = Console()
    primary = current_theme.colors.get("primary", "cyan")
    secondary = current_theme.colors.get("secondary", "green")
    
    cmd_info = CLI_COMMANDS.get(command_name)
    if not cmd_info:
        console.print(f"[red]Command '{command_name}' not found[/red]")
        return
    
    # Build detailed help text using proper Rich styling
    from rich.text import Text
    
    title_text = f"ℹ️  {cmd_info['name']} Help"
    details = Text()
    details.append(f"Command: {cmd_info['name']}\n\n", style=f"bold {primary}")
    details.append(f"Description:\n{cmd_info['description']}\n\n", style=f"bold {primary}")
    details.append(f"Usage:\n  ", style=f"bold {primary}")
    details.append(f"{cmd_info['usage']}\n", style="cyan")
    
    if cmd_info.get("aliases"):
        aliases = ", ".join(cmd_info["aliases"])
        details.append(f"\nAliases: {aliases}", style=f"bold {primary}")
    
    panel = Panel(
        details,
        title=title_text,
        border_style=primary,
        box=box.ROUNDED,
    )
    console.print(panel)


def show_all_shortcuts_menu():
    """Show shortcuts for all menus."""
    import questionary
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from gitpush.ui.banner import current_theme
    _, MAIN_MENU_STYLE = _get_menu_styles()
    
    console = Console()
    primary = current_theme.colors.get("primary", "cyan")
    
    menu_options = [
        ("main_menu", "Main Menu"),
        ("branch_menu", "Branch Operations"),
        ("ai_menu", "AI Menu"),
        ("advanced_menu", "Advanced Tools"),
    ]
    
    # Let user choose which menu's shortcuts to view
    choice = questionary.select(
        "Select a menu to view shortcuts:",
        choices=[name for _, name in menu_options] + ["🔙 Back"],
        qmark="➜",
        pointer="►",
        style=MAIN_MENU_STYLE,
    ).ask()
    
    if not choice or "Back" in choice:
        return
    
    # Find the menu key
    menu_key = None
    for key, name in menu_options:
        if name == choice:
            menu_key = key
            break
    
    if menu_key:
        show_shortcuts_table(menu_key)


# ══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "CLI_COMMANDS",
    "MENU_SHORTCUTS",
    "NAVIGATION_KEYS",
    "QUICK_REFERENCE",
    "get_command_help",
    "get_all_commands",
    "get_menu_shortcuts",
    "show_command_list",
    "show_shortcuts_table",
    "show_quick_reference",
    "show_help_menu",
    "show_command_details",
    "show_all_shortcuts_menu",
]
