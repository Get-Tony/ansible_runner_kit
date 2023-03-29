"""Ansible-Runner Kit Host Operations."""

from typing import Union

import click
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

from src import constants as c


def get_host(target_host: str) -> Union[Host, None]:
    """Get a host from the inventory."""
    data_loader = DataLoader()
    inventory = InventoryManager(loader=data_loader, sources=[c.INVENTORY_DIR])
    return inventory.get_host(target_host)


def get_groups_for_host(host: Host) -> list[str]:
    """Get all groups a host is a member of."""
    groups = []
    for group in host.groups:
        groups.append(group.name)
    return groups


def display_groups(target_host: str, groups: list[str]) -> None:
    """Display all groups a host is a member of."""
    click.echo(f"Host '{target_host}' is a member of the following groups:")
    for group in groups:
        click.echo(f"- {group}")


def get_group(target_group: str) -> Union[Group, None]:
    """Get a group from the inventory."""
    data_loader = DataLoader()
    inventory = InventoryManager(loader=data_loader, sources=[c.INVENTORY_DIR])
    return inventory.groups.get(target_group)


def get_hosts_for_group(group: Group) -> list[Union[Host, None]]:
    """Get all hosts in a group."""
    host_list: list[Union[Host, None]] = []
    host_list = group.get_hosts()
    return host_list


def display_hosts(target_group: str, hosts: list[Union[Host, None]]) -> None:
    """Display all hosts in a group."""
    click.echo(f"Group '{target_group}' contains the following hosts:")
    for host in hosts:
        click.echo(f"- {host}")
