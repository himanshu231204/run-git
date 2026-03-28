"""
Command modules for gitpush CLI.
"""
from gitpush.commands.push import push
from gitpush.commands.init import init_command
from gitpush.commands.status import status, log
from gitpush.commands.branch import branch, switch, merge
from gitpush.commands.remote import remote, pull, sync
from gitpush.commands.stash import stash, undo
from gitpush.commands.github import new
from gitpush.commands.theme import theme
from gitpush.commands.graph import graph

__all__ = [
    'push',
    'init_command',
    'status',
    'log',
    'branch',
    'switch',
    'merge',
    'remote',
    'pull',
    'sync',
    'stash',
    'undo',
    'new',
    'theme',
    'graph',
]
