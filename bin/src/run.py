"""Ansible-Runner Kit run command."""

from pathlib import Path

import ansible_runner

from src import constants as c


def prepare_extra_vars(extra_vars: str) -> dict[str, str]:
    """Prepare extra variables for the playbook."""
    extra_vars_dict = {}
    if extra_vars:
        extra_vars_list = extra_vars.split(",")
        for pair in extra_vars_list:
            key, value = pair.split("=")
            extra_vars_dict[key] = value

    return extra_vars_dict


def run_ansible_playbook(
    playbook_path: Path,
    rotate_artifacts: int,
    limit: str,
    extra_vars_dict: dict[str, str],
) -> None:
    """Run an Ansible playbook using ansible-runner."""
    ansible_runner.run(
        private_data_dir=str(c.ARK_DIR),
        playbook=str(playbook_path),
        rotate_artifacts=rotate_artifacts,
        limit=limit,
        extravars=extra_vars_dict if extra_vars_dict else None,
    )
