"""Ansible-Runner Kit Constants."""

from pathlib import Path

ARK_DIR: Path = Path(__file__).parent.parent.parent
PROJECT_DIR: Path = ARK_DIR / "project"
ARK_INTERPRETER: Path = ARK_DIR / ".venv" / "bin" / "python"
RUNNER_EXECUTABLE: str = "ansible-runner"
INVENTORY_DIR: str = "inventory"
CRONJOB_TAG: str = "#ARK-"
