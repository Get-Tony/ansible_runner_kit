#!/usr/bin/env python3
"""ARK - Ansible Runner Kit."""
__author__ = "Anthony Pagan <Get-Tony@outlook.com>"


import getpass
import subprocess
from typing import Optional, Union

import click
from ansible.inventory.host import Host
from src import constants as c
from src.cron import manage_cron_jobs
from src.inventory import (
    display_groups,
    display_hosts,
    get_group,
    get_groups_for_host,
    get_host,
    get_hosts_for_group,
)
from src.lint import (
    is_ansible_lint_installed,
    lint_all_playbooks,
    lint_single_playbook,
)
from src.run import prepare_extra_vars, run_ansible_playbook
from src.utils import (
    display_artifact_report,
    find_artifacts,
    get_playbook_path,
    sort_and_limit_artifacts,
    validate_inventory_dir,
    validate_playbook,
    validate_project,
)


@click.group()
def cli() -> None:
    """ARK - Ansible Runner Kit."""


# Run command
@cli.command()
@click.argument("playbook_file", type=click.Path(exists=False), default="")
@click.option(
    "--rotate-artifacts",
    default=7,
    type=click.IntRange(1, 31),
    help="Number of artifacts to keep.",
)
@click.option(
    "--limit",
    default="",
    type=str,
    help="Limit the playbook execution to a specific group or host.",
)
@click.option(
    "--extra-vars",
    default="",
    type=str,
    help="Pass additional variables as key-value pairs.",
)
def run(
    playbook_file: str, rotate_artifacts: int, limit: str, extra_vars: str
) -> None:
    """Run an Project playbook."""
    validate_project()

    playbook_path = get_playbook_path(playbook_file)
    if not playbook_path:
        return

    extra_vars_dict = prepare_extra_vars(extra_vars)
    run_ansible_playbook(
        playbook_path, rotate_artifacts, limit, extra_vars_dict
    )


# Lint command
@cli.command()
@click.argument("playbook_file", type=click.Path(exists=False), default="")
def lint(playbook_file: str) -> None:
    """Lint an Project playbooks using ansible-lint."""
    if not is_ansible_lint_installed():
        return

    if playbook_file:
        lint_single_playbook(playbook_file)
    else:
        lint_all_playbooks()


@cli.command()
@click.option(
    "--artifacts-dir",
    default="artifacts",
    help="Path to the artifacts directory.",
)
@click.option(
    "--last",
    type=int,
    default=None,
    help="Display the last x reports.",
)
def report(artifacts_dir: str, last: Optional[int]) -> None:
    """Display Ansible run report(s)."""
    artifact_folders = find_artifacts(artifacts_dir)
    artifact_folders = sort_and_limit_artifacts(artifact_folders, last)

    for artifact_path in artifact_folders:
        display_artifact_report(artifact_path)


@click.group()
def inv() -> None:
    """Inventory commands."""


@inv.command()
@click.argument("target_host")
def get_host_groups(target_host: str) -> None:
    """
    Display all groups a host is a member of.
    """
    validate_inventory_dir()
    host = get_host(target_host)

    if not host:
        click.echo(f"Host '{target_host}' not found in the inventory.")
        return

    groups = get_groups_for_host(host)
    display_groups(target_host, groups)


@inv.command()
@click.argument("target_group")
def get_group_hosts(target_group: str) -> None:
    """
    Display all hosts in a group.
    """
    validate_inventory_dir()
    group = get_group(target_group)

    if not group:
        click.echo(f"Group '{target_group}' not found in the inventory.")
        return

    hosts: list[Union[Host, None]] = get_hosts_for_group(group)
    display_hosts(target_group, hosts)


@click.group()
def cron() -> None:
    """Manage cron jobs."""


@cron.command("create")
@click.option(
    "--user",
    default=getpass.getuser(),
    help="The user for the cron job.",
    required=True,
)
@click.option("--name", help="The name of the cron job.", required=True)
@click.option(
    "--job",
    help="The command to be executed.",
    callback=validate_playbook,
    required=True,
)
@click.option("--minute", default="*", help="Minute field of the cron job.")
@click.option("--hour", default="*", help="Hour field of the cron job.")
@click.option(
    "--day", default="*", help="Day of the month field of the cron job."
)
@click.option("--month", default="*", help="Month field of the cron job.")
@click.option(
    "--weekday", default="*", help="Day of the week field of the cron job."
)
def create(user: str, name: str, job: str, **kwargs: str) -> None:
    """Create a cron job."""
    manage_cron_jobs(
        user,
        add_or_update_jobs=[
            {
                "name": name,
                "job": job,
                "minute": kwargs["minute"],
                "hour": kwargs["hour"],
                "day": kwargs["day"],
                "month": kwargs["month"],
                "weekday": kwargs["weekday"],
            }
        ],
        remove_jobs=None,
    )


@cron.command("delete")
@click.option(
    "--user",
    default=getpass.getuser(),
    help="The user for the cron job.",
    required=True,
)
@click.option(
    "--name", help="The name of the cron job to delete.", required=True
)
def delete(user: str, name: str) -> None:
    """Delete a cron job."""
    manage_cron_jobs(user, remove_jobs=[name], add_or_update_jobs=None)


@cron.command("list")
@click.option(
    "--user",
    default=getpass.getuser(),
    help="The user for the cron job.",
    required=True,
)
def list_cron_jobs(user: str) -> None:
    """List all ARK cron jobs for a user."""
    click.echo(f"ARK cron jobs for user {user}:")
    try:
        cron_list = subprocess.check_output(
            ["crontab", "-u", user, "-l"], text=True
        ).splitlines()
    except subprocess.CalledProcessError as cron_list_error:
        if cron_list_error.returncode == 1:
            return
        click.echo("An error occurred while fetching the cron jobs.")
        return

    for line in cron_list:
        if c.CRONJOB_TAG in line:
            click.echo(line)


cli.add_command(inv)
cli.add_command(cron)

if __name__ == "__main__":
    cli()
