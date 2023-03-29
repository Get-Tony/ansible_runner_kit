"""Ansible-Runner Kit Cron Operations."""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

import click

from src import constants as c


def read_cron_list(user: str) -> List[str]:
    """Read the list of cron jobs for a user."""
    try:
        cron_list = subprocess.check_output(
            ["crontab", "-u", user, "-l"], text=True
        ).splitlines()
    except subprocess.CalledProcessError as cron_err:
        if cron_err.returncode == 1:
            cron_list = []
        else:
            raise cron_err
    return cron_list


def add_or_update_cron_jobs(
    cron_list: List[str], add_or_update_jobs: List[Dict[str, str]]
) -> List[str]:
    """Add or update cron jobs."""
    python_interpreter = str(c.ARK_INTERPRETER)
    ark_script = str(c.PROJECT_DIR / "bin" / "ark.py")

    for job in add_or_update_jobs:
        cron_line = (
            f"{job['minute']} {job['hour']} {job['day']} "
            f"{job['month']} {job['weekday']} {python_interpreter} "
            f"{ark_script} run {job['job']} "
            f"{c.CRONJOB_TAG}{job['name']}"
        )
        found = False
        for i, line in enumerate(cron_list):
            if line.lower().endswith(
                f"{c.CRONJOB_TAG.lower()}{job['name'].lower()}"
            ):
                cron_list[i] = cron_line
                found = True
                break
        if not found:
            cron_list = check_for_duplicates(cron_list, job, cron_line)
    return cron_list


def check_for_duplicates(
    cron_list: List[str], job: Dict[str, str], cron_line: str
) -> List[str]:
    """Check for duplicate cron jobs and warn if found."""
    duplicate_name = False
    for line in cron_list:
        if line.lower().endswith(
            f"{c.CRONJOB_TAG.lower()}{job['name'].lower()}"
        ):
            duplicate_name = True
            click.echo(
                f"Warning: Job with the name '{job['name']}' "
                "already exists. Not Creating."
            )
            break
    if not duplicate_name:
        cron_list.append(cron_line)
    return cron_list


def remove_cron_jobs(
    cron_list: List[str], remove_jobs: List[str]
) -> List[str]:
    """Remove specified cron jobs."""
    for unwanted_job in remove_jobs:
        for i, line in enumerate(cron_list):
            if line.lower().endswith(
                f"{c.CRONJOB_TAG.lower()}{unwanted_job.lower()}"
            ):
                del cron_list[i]
                break
    return cron_list


def update_crontab(user: str, cron_list: List[str]) -> None:
    """Update the user's crontab with the modified cron list."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        temp.writelines([f"{line}\n" for line in cron_list])
        temp.flush()
        subprocess.run(["crontab", "-u", user, temp.name], check=True)
    Path(temp.name).unlink()


def manage_cron_jobs(
    user: str,
    add_or_update_jobs: Optional[List[Dict[str, str]]],
    remove_jobs: Optional[List[str]],
) -> None:
    """Manage cron jobs for a user."""
    cron_list = read_cron_list(user)

    if add_or_update_jobs:
        cron_list = add_or_update_cron_jobs(cron_list, add_or_update_jobs)

    if remove_jobs:
        cron_list = remove_cron_jobs(cron_list, remove_jobs)

    update_crontab(user, cron_list)
