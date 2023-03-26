#!.venv/bin/python
"""Ansible Runner Kit CLI."""
import subprocess
import sys
from pathlib import Path
from typing import List

try:
    import ansible_runner
    import click
    from ansible.inventory.manager import InventoryManager
    from ansible.parsing.dataloader import DataLoader
except ImportError as error:
    print(f"Error: {error}")
    print("Please run 'setup.sh' to setup the environment.")
    sys.exit(1)

ARK_DIR: Path = Path.cwd().resolve()
PROJECT_DIR: Path = ARK_DIR / "project"
RUNNER_EXECUTABLE: str = "ansible-runner"
INVENTORY_DIR: str = "inventory"


def validate_inventory_dir() -> None:
    """Check if the inventory directory exists."""
    if not Path(INVENTORY_DIR).is_dir():
        click.echo(f"Inventory directory '{INVENTORY_DIR}' does not exist.")
        sys.exit(1)


def find_playbooks() -> List[str]:
    """Find all YAML or YML playbooks in the playbook directory."""
    playbooks: List[str] = []
    for playbook in PROJECT_DIR.glob("*.yml"):
        playbooks.append(playbook.name)
    for playbook in PROJECT_DIR.glob("*.yaml"):
        playbooks.append(playbook.name)
    return playbooks


@click.group()
def cli() -> None:
    """Playbook Manager CLI."""


@cli.command()
@click.argument("playbook_file", type=click.Path(exists=False), default="")
@click.option(
    "--rotate-artifacts",
    default=7,
    type=click.IntRange(1, 31),
    help="Number of artifacts to keep.",
)
def run(playbook_file: str, rotate_artifacts: int) -> None:
    """Run an Ansible playbook using ansible-runner."""
    if not playbook_file:
        click.echo("List of available playbooks:")
        for playbook in find_playbooks():
            click.echo(f" - {playbook}")
        return

    # Check if the playbook file exists in the playbook directory
    playbook_path: Path = PROJECT_DIR / playbook_file
    if not playbook_path.is_file():
        click.echo(f"Invalid argument: '{playbook_file}' was not found.")
        click.echo("List of available playbooks:")
        for playbook in find_playbooks():
            click.echo(f" - {playbook}")
        return

    # Run the specified playbook
    ansible_runner.run(
        private_data_dir=str(ARK_DIR),
        playbook=str(playbook_path),
        rotate_artifacts=rotate_artifacts,
    )


@cli.command()
@click.argument("playbook_file", type=click.Path(exists=False), default="")
def lint(playbook_file: str) -> None:
    """Lint an Ansible playbook using ansible-lint."""
    try:
        # Check if ansible-lint is installed and get its version
        subprocess.check_output(["ansible-lint", "--version"])
    except subprocess.CalledProcessError:
        click.echo("Warning: ansible-lint is not installed.")
        return

    if playbook_file:
        # Check if the playbook file exists in the playbook directory
        playbook_path: Path = PROJECT_DIR / playbook_file
        if not playbook_path.is_file():
            click.echo(f"Invalid argument: '{playbook_file}' was not found.")
            click.echo("List of available playbooks:")
            for playbook in find_playbooks():
                click.echo(f" - {playbook}")
            return

        # Lint the specified playbook
        try:
            subprocess.check_output(["ansible-lint", str(playbook_path)])
        except subprocess.CalledProcessError as error:
            click.echo(f"Error linting playbook '{playbook_file}': {error}")
    else:
        # Lint all playbooks in the project directory
        for playbook in find_playbooks():
            playbooks_path: Path = PROJECT_DIR / playbook
            try:
                subprocess.check_output(["ansible-lint", str(playbooks_path)])
            except subprocess.CalledProcessError as error:
                click.echo(f"Error linting playbook '{playbook}': {error}")


@cli.command()
@click.argument("target_host")
def get_host_groups(target_host: str) -> None:
    """
    Display all groups a host is a member of.
    """
    validate_inventory_dir()
    # Initialize DataLoader and InventoryManager
    data_loader = DataLoader()
    inventory = InventoryManager(loader=data_loader, sources=[INVENTORY_DIR])

    # Get host object
    host = inventory.get_host(target_host)

    if not host:
        print(f"Host '{target_host}' not found in the inventory.")
        return

    # Collect the groups the host is a member of
    groups = []
    for group in host.groups:
        groups.append(group.name)

    click.echo(f"Host '{target_host}' is a member of the following groups:")
    for group in groups:
        click.echo(f"- {group}")


@cli.command()
@click.argument("target_group")
def get_group_hosts(target_group: str) -> None:
    """
    Display all hosts in a group.
    """
    validate_inventory_dir()
    # Initialize DataLoader and InventoryManager
    data_loader = DataLoader()
    inventory = InventoryManager(loader=data_loader, sources=[INVENTORY_DIR])

    # Get group object
    group = inventory.groups.get(target_group)

    if not group:
        print(f"Group '{target_group}' not found in the inventory.")
        return

    # Collect all hosts in the group, including nested and child groups
    hosts = group.get_hosts()

    click.echo(f"Group '{target_group}' contains the following hosts:")
    for host in hosts:
        click.echo(f"- {host.name}")


if __name__ == "__main__":
    cli()
