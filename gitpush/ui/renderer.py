"""Renderer primitives for the interactive terminal UI."""

from dataclasses import dataclass
from typing import List

import questionary
from questionary import Choice, Separator
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule


@dataclass
class MenuItem:
    """Single action row in a menu section."""

    key: str
    icon: str
    label: str
    description: str


@dataclass
class MenuSection:
    """Logical group of menu items."""

    title: str
    items: List[MenuItem]


class CompactDashboardRenderer:
    """Compact, keyboard-first renderer inspired by modern coding CLIs."""

    def __init__(self, console: Console):
        self.console = console

    @staticmethod
    def _to_ascii_icon(icon: str) -> str:
        """Map emoji-heavy icons to stable ASCII-friendly symbols."""
        icon_map = {
            "🚀": ">",
            "🤖": "*",
            "📊": "#",
            "🌿": "+",
            "🔄": "~",
            "🌳": "@",
            "🆕": "+",
            "📥": "v",
            "🔧": "~",
            "⚙️": "o",
            "📚": "?",
            "❌": "x",
            "➕": "+",
            "🗑️": "-",
            "🔀": "~",
            "⬅️": "<",
        }
        return icon_map.get(icon, "*")

    @staticmethod
    def _clip_text(text: str, max_len: int) -> str:
        """Clip text to max length while preserving readability."""
        if max_len <= 0:
            return ""
        if len(text) <= max_len:
            return text
        if max_len <= 3:
            return text[:max_len]
        return f"{text[: max_len - 3]}..."

    def _format_menu_line(self, item: MenuItem, width: int) -> str:
        """Build a compact, width-aware menu line."""
        icon = self._to_ascii_icon(item.icon)

        # Keep labels aligned while adapting to terminal width.
        label_width = max(12, min(20, width // 4))
        label = self._clip_text(item.label, label_width)

        # Reserve room for icon + spacing + separator and avoid hard wraps.
        reserved = 6 + label_width
        desc_width = max(16, width - reserved)
        description = self._clip_text(item.description, desc_width)
        return f"{icon} {label:<{label_width}} {description}"

    def render_header(self, title: str, border_color: str = "cyan", breadcrumb: str = "") -> None:
        """Render a compact dashboard header."""
        self.console.print(Rule(style=border_color))
        panel = Panel(
            f"[bold {border_color}]run-git[/bold {border_color}]  [dim]- {title}[/dim]",
            border_style=border_color,
            padding=(0, 1),
        )
        self.console.print(panel)
        if breadcrumb:
            self.console.print(f"[dim]{breadcrumb}[/dim]")
        self.console.print("[dim]Use arrows to navigate, Enter to select, q to quit[/dim]\n")

    def render_repo_context(
        self,
        repo_name: str,
        branch_name: str,
        total_changes: int,
        is_repo: bool,
        border_color: str = "cyan",
    ) -> None:
        """Render compact repository context block."""
        if not is_repo:
            self.console.print(
                Panel(
                    "[bold red]Not a git repository[/bold red]\n"
                    "[dim]Run run-git init or move into an existing repository.[/dim]",
                    title="Context",
                    border_style="red",
                    padding=(0, 1),
                )
            )
            return

        status = "clean" if total_changes == 0 else f"{total_changes} change(s)"
        status_style = "green" if total_changes == 0 else "yellow"

        body = (
            f"[bold]repo[/bold]: {repo_name}    "
            f"[bold]branch[/bold]: {branch_name}    "
            f"[bold]status[/bold]: [{status_style}]{status}[/{status_style}]"
        )
        self.console.print(
            Panel(
                body,
                title="Context",
                border_style=border_color,
                padding=(0, 1),
            )
        )

    def select_menu(self, sections: List[MenuSection], style) -> str:
        """Render a compact grouped menu and return selected action key."""
        choices = []
        terminal_width = getattr(self.console.size, "width", 100)
        line_width = max(50, terminal_width - 8)

        for section in sections:
            choices.append(Separator(f"-- {section.title} --"))
            for item in section.items:
                choices.append(
                    Choice(title=self._format_menu_line(item, line_width), value=item.key)
                )

        selected = questionary.select(
            "",
            choices=choices,
            qmark=">",
            pointer=">",
            style=style,
        ).ask()

        if selected == "b":
            return "back"
        if selected == "q":
            return "quit"
        return selected or ""
