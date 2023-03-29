"""DNS resolution check for Ansible inventories."""
__author__ = "Anthony Pagan <Get-Tony@outlook.com>"

import argparse
import csv
import subprocess
from typing import List

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


def check_host(host: str, dns_servers: List[str], timeout: int) -> List[str]:
    """Check if a host is resolvable by a list of DNS servers."""
    missing_servers = []
    for server in dns_servers:
        try:
            resolved = subprocess.run(
                ["nslookup", host, server],
                capture_output=True,
                timeout=timeout,
                check=True,
            )
            if resolved.returncode == 1:
                continue
        except subprocess.TimeoutExpired:
            missing_servers.append(server)
        except subprocess.CalledProcessError:
            missing_servers.append(server)

    return missing_servers


def get_inventory(args: argparse.Namespace) -> List[str]:
    """Get a list of hosts from an Ansible inventory file."""
    inventory_file = args.inventory
    data_loader = DataLoader()
    inventory = InventoryManager(loader=data_loader, sources=inventory_file)
    hosts = sorted([host.name for host in inventory.get_hosts()])
    return hosts


def main() -> None:
    """Check Ansible inventory hosts for DNS resolution."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inventory", help="The inventory file or target folder"
    )
    parser.add_argument(
        "dns_servers", help="Comma-separated list of DNS servers"
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=5,
        help="Timeout for each check (default 5 seconds)",
    )
    parser.add_argument("--output", "-o", help="Output CSV file")
    args = parser.parse_args()

    try:
        dns_servers = args.dns_servers.split(",")
    except ValueError as value_error:
        print(f"Error: Invalid DNS servers list - {value_error}")
        return

    try:
        hosts = get_inventory(args)
    except FileNotFoundError as file_error:
        print(f"Error: Inventory file not found - {file_error}")
        return

    results = []
    for host in hosts:
        try:
            missing_servers = check_host(host, dns_servers, args.timeout)
        except (
            subprocess.TimeoutExpired,
            subprocess.CalledProcessError,
        ) as timeout_error:
            print(f"Error: Issue with DNS resolution check - {timeout_error}")
            continue
        except ValueError as value_error:
            print(f"Error: Invalid input value - {value_error}")
            continue

        if missing_servers:
            results.append([host, ", ".join(missing_servers)])

    if args.output:
        try:
            with open(
                args.output, "w", newline="", encoding="utf-8"
            ) as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Hostname", "No resolution with"])
                writer.writerows(results)
        except FileNotFoundError as file_error:
            print(f"Error: Output file not found - {file_error}")
        except PermissionError as perm_error:
            print(f"Error: Permission denied for output file - {perm_error}")
    else:
        print("Hostname, No resolution with")
        for row in results:
            print(",".join(row))


if __name__ == "__main__":
    main()
