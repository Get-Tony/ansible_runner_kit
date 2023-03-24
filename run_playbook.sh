#!/bin/bash

# Constants
VENV_DIR=".venv"
PYTHON_EXECUTABLE="python3"
ANSIBLE_RUNNER_EXECUTABLE="ansible-runner"
PROJECT_DIR="$(pwd)/project"
ROTATE_ARTIFACTS="7"

# Check if the playbook argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <playbook_file>"
    exit 1
fi

PLAYBOOK="$1"
PLAYBOOK_PATH="$PROJECT_DIR/$PLAYBOOK"

# Check if the playbook file exists in the project directory
if [ ! -f "$PLAYBOOK_PATH" ]; then
    echo "Invalid argument: playbook file '$PLAYBOOK' not found in the project directory."
    exit 1
fi

# Activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Please create the virtual environment before running the script."
    exit 1
fi

source "$VENV_DIR/bin/activate"

# Check if ansible-runner is installed
if ! command -v "$ANSIBLE_RUNNER_EXECUTABLE" &>/dev/null; then
    echo "ansible-runner not found. Please install ansible-runner in the virtual environment."
    deactivate
    exit 1
fi

# Run ansible-runner with specified flags
"$ANSIBLE_RUNNER_EXECUTABLE" run . -p "$PLAYBOOK" --rotate-artifacts "$ROTATE_ARTIFACTS"

# Deactivate virtual environment
deactivate
