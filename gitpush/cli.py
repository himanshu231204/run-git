"""
Main CLI interface for run-git - Git Made Easy
"""
import click

from gitpush import __version__
from gitpush.ui.banner import show_banner
from gitpush.commands import (
    push,
    init_command,
    status,
    log,
    branch,
    switch,
    merge,
    remote,
    pull,
    sync,
    stash,
    undo,
    new,
    theme,
    graph,
)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', '-v', is_flag=True, help='Show version')
def main(ctx, version):
    """run-git - Git Made Easy"""
    if version:
        click.echo(f"run-git version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        show_banner()
        from gitpush.ui.interactive import InteractiveUI
        interactive_mode = InteractiveUI()
        interactive_mode.main_menu()


# Register commands
main.add_command(push)
main.add_command(init_command)
main.add_command(status)
main.add_command(log)
main.add_command(branch)
main.add_command(switch)
main.add_command(merge)
main.add_command(remote)
main.add_command(pull)
main.add_command(sync)
main.add_command(stash)
main.add_command(undo)
main.add_command(new)
main.add_command(theme)
main.add_command(graph)


if __name__ == '__main__':
    main()
