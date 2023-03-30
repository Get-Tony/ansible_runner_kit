"""Ansible-Runner Kit Utilities."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

import click

from . import constants as c


def find_playbooks() -> List[str]:
    """Find all YAML or YML playbooks in the project directory."""
    playbooks: List[str] = []
    for playbook in c.PROJECT_DIR.glob("*.yml"):
        playbooks.append(playbook.name)
    for playbook in c.PROJECT_DIR.glob("*.yaml"):
        playbooks.append(playbook.name)
    return playbooks


def validate_project() -> None:
    """Check if the current directory is a valid Ansible-Runner input tree."""
    required_dirs = [
        c.ARK_DIR / "project",
        c.ARK_DIR / "inventory",
        c.ARK_DIR / "env",
    ]
    required_files = [
        c.ARK_DIR / "project" / "main.yml",
        c.ARK_DIR / "env" / "envvars",
        c.ARK_DIR / "env" / "ssh_key",
    ]
    missing_dirs: List[Union[str, Path]] = []
    missing_files: List[Union[str, Path]] = []

    # Check for required directories
    for required_dir in required_dirs:
        if not required_dir.is_dir():
            missing_dirs.append(required_dir)

    # Check for required files
    for required_file in required_files:
        if not required_file.is_file():
            missing_files.append(required_file)

    # Report missing directories and files, then exit if any are missing
    if any(missing_dirs or missing_files):
        if missing_dirs:
            click.echo("\nRequired directories are missing:")
            for dir_ in missing_dirs:
                click.echo(f"  {dir_}")
        if missing_files:
            click.echo("\nRequired files are missing:")
            for file_ in missing_files:
                click.echo(f"  {file_}")
        click.echo("\nPlease correct the issues above then try again.")
        sys.exit(1)


def get_playbook_path(playbook_file: str) -> Union[Path, None]:
    """Get the path to the playbook file."""
    playbook_path: Path = c.PROJECT_DIR / playbook_file
    if not playbook_path.is_file():
        click.echo(f"Invalid argument: '{playbook_file}' was not found.")
        list_available_playbooks(playbook_file)
        return None

    return playbook_path


def list_available_playbooks(playbook_file: str) -> None:
    """List all available playbooks in the project directory."""
    if not playbook_file:
        click.echo("List of available playbooks:")
        for playbook in find_playbooks():
            click.echo(f" - {playbook}")


def validate_inventory_dir() -> None:
    """Check if the inventory directory exists."""
    if not Path(c.INVENTORY_DIR).is_dir():
        click.echo(f"Inventory directory '{c.INVENTORY_DIR}' does not exist.")
        sys.exit(1)


def find_artifacts(artifacts_dir: str) -> List[Path]:
    """Find all artifact folders in the artifacts directory."""
    artifact_root_path = Path(artifacts_dir)
    artifact_folders = [
        path
        for path in artifact_root_path.glob("**")
        if (path / "stdout").is_file()
    ]
    return artifact_folders


def sort_and_limit_artifacts(
    artifact_folders: List[Path], last: Optional[int]
) -> List[Path]:
    """Sort artifacts by timestamp and limit to the last N artifacts."""
    artifact_folders.sort(
        key=lambda folder: folder.stat().st_mtime, reverse=True
    )

    if 0 < last < len(artifact_folders) if last is not None else False:
        artifact_folders = artifact_folders[:last]

    return artifact_folders


def extract_playbook_name_from_file(file_path: str) -> Optional[str]:
    """Extract the playbook name from the command file."""
    file_ = Path(file_path)

    if not file_.exists():
        return None

    with file_.open(encoding="utf-8") as command_file:
        content = command_file.read()

    data = json.loads(content)
    command_string = " ".join(data["command"])
    match = re.search(
        r"project/([\w-]+\.yml)",
        command_string,
    )

    if match:
        return match.group(1)
    print("Playbook name not found in the command string.")
    return None


def display_artifact_report(artifact_path: Path) -> None:
    """Display the report for a single artifact folder."""
    stdout_path: Path = artifact_path / "stdout"

    with stdout_path.open("r", encoding="utf-8") as stdout_file:
        content = stdout_file.read()

    play_recaps = extract_play_recaps(content)
    timestamp = get_artifact_timestamp(stdout_path)
    playbook_name = extract_playbook_name_from_file(
        str(artifact_path / "command")
    )

    click.echo(f"Report for {artifact_path}:")
    click.echo(f"{playbook_name or 'Playbook'} executed at: {timestamp}")
    click.echo("-------------------------")

    for recap in play_recaps:
        host_stats = extract_host_stats(recap)
        for host, stats in host_stats.items():
            click.echo(f"{host}: {stats}")
    click.echo("")


def extract_play_recaps(content: str) -> List[str]:
    """Extract the play recap from the stdout file content."""
    play_recap_regex = re.compile(
        r"PLAY RECAP\s+\*+\s+(?P<recap>.*?)(\n\n|$)", re.DOTALL
    )
    play_recaps = play_recap_regex.findall(content)
    return [recap_tuple[0] for recap_tuple in play_recaps]


def get_artifact_timestamp(stdout_path: Path) -> str:
    """Get the timestamp of the artifact's stdout file."""
    mod_time = stdout_path.stat().st_mtime
    return datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")


def extract_host_stats(recap: str) -> dict[str, dict[str, int]]:
    """Extract the host stats from the play recap."""
    lines = recap.strip().split("\n")
    host_stats = {}

    for line in lines:
        host, stats = line.strip().split(":", 1)
        stats_dict = {}
        for stat in stats.strip().split(" "):
            if "=" in stat:
                key_, value_ = stat.split("=")
                stats_dict[key_] = int(value_)
        host_stats[host.strip()] = stats_dict

    return host_stats


def validate_playbook(
    # Callback function. ctx and param are required even if unused!
    ctx: click.Context,  # pylint: disable=unused-argument
    param: click.Parameter,  # pylint: disable=unused-argument
    value: str,
) -> str:
    """Validate the playbook argument."""
    valid_playbooks = find_playbooks()
    if value not in valid_playbooks:
        raise click.BadParameter(
            f"Invalid playbook: {value}. Valid playbooks in the project "
            f"directory are: {', '.join(valid_playbooks)}"
        )
    return value
