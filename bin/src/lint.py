"""Linting functions for Ansible playbooks."""

import subprocess
from pathlib import Path

import click

from src import constants as c
from src.utils import find_playbooks, get_playbook_path


def is_ansible_lint_installed() -> bool:
    """Check if ansible-lint is installed."""
    try:
        subprocess.check_output(["ansible-lint", "--version"])
        return True
    except subprocess.CalledProcessError:
        click.echo("Warning: ansible-lint is not installed.")
        return False


def lint_single_playbook(playbook_file: str) -> None:
    """Lint a single playbook."""
    playbook_path = get_playbook_path(playbook_file)
    if not playbook_path:
        return

    try:
        subprocess.check_output(["ansible-lint", str(playbook_path)])
    except subprocess.CalledProcessError as single_error:
        click.echo(f"Error linting playbook '{playbook_file}': {single_error}")


def lint_all_playbooks() -> None:
    """Lint all playbooks in the project directory."""
    for playbook in find_playbooks():
        playbooks_path: Path = c.PROJECT_DIR / playbook
        try:
            subprocess.check_output(["ansible-lint", str(playbooks_path)])
        except subprocess.CalledProcessError as list_error:
            click.echo(f"Error linting playbook '{playbook}': {list_error}")
