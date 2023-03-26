#!/bin/bash

# Constants
MIN_PYTHON_VERSION="3.9.2"
VENV_DIR_NAME=".venv"
VENV_PROMPT="Ansible-Runner"
REQUIREMENTS_FILE="requirements.txt"
DEV_REQUIREMENTS_FILE="requirements.dev.txt"
PYTHON_EXECUTABLE="python3"
PIP_EXECUTABLE="pip"

# Functions

function usage() {
    echo "Usage: $0 [--dev]"
    echo "This script will create a virtual environment and install packages from the requirements.txt file."
    echo "If the --dev argument is passed, it will also install packages from the requirements.dev.txt file."
    echo "If a valid virtual environment already exists, it will be used."
    exit 1
}

function check_python() {
    if ! command -v "$PYTHON_EXECUTABLE" &>/dev/null; then
        echo "$PYTHON_EXECUTABLE is not installed. Please install $PYTHON_EXECUTABLE $MIN_PYTHON_VERSION or later."
        exit 1
    fi

    PYTHON_VERSION=$("$PYTHON_EXECUTABLE" -V 2>&1 | awk '{print $2}')
    if [ "$(printf '%s\n' "$MIN_PYTHON_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_PYTHON_VERSION" ]; then
        echo "$PYTHON_EXECUTABLE version is too old. Please upgrade to $PYTHON_EXECUTABLE $MIN_PYTHON_VERSION or later."
        exit 1
    fi

    echo "$PYTHON_EXECUTABLE $MIN_PYTHON_VERSION or later is installed."
}

function check_venv_module() {
    if ! "$PYTHON_EXECUTABLE" -c 'import venv' &>/dev/null; then
        echo "venv module is not available. Please install it and try again."
        exit 1
    fi

    echo "venv module is available."
}

function create_venv() {
    if [ ! -d "$VENV_DIR_NAME" ]; then
        echo "Creating virtual environment..."
        if ! "$PYTHON_EXECUTABLE" -m venv "$VENV_DIR_NAME" --prompt "$VENV_PROMPT"; then
            echo "Failed to create virtual environment."
            exit 1
        fi
    else
        # Check if the virtual environment directory has a pyvenv.cfg file
        if [ ! -f "$VENV_DIR_NAME/pyvenv.cfg" ]; then
            echo "Virtual environment directory already exists but does not have a pyvenv.cfg file."
            echo "Please delete or move the $VENV_DIR_NAME directory and try again."
            exit 1
        fi
        #VENV_PROMPT_LINE=$(grep -oP '(?<=^prompt\s=\s).*' "$VENV_DIR_NAME/pyvenv.cfg")
        VENV_PROMPT_LINE=$(grep -oP '(?<=^prompt\s=\s).*' "$VENV_DIR_NAME/pyvenv.cfg" | sed 's/[^[:alnum:]-]//g')
        echo "Virtual environment file: $VENV_PROMPT_LINE"
        if [ "$VENV_PROMPT_LINE" == "$VENV_PROMPT" ]; then
            echo "Virtual environment directory with the expected prompt already exists."
            echo "Using the existing virtual environment."
        else
            echo "Virtual environment directory already exists but has a different prompt."
            echo "Please delete or move the $VENV_DIR_NAME directory and try again."
            exit 1
        fi
    fi
}

function activate_venv() {
    echo "Activating virtual environment..."
    if ! source "$VENV_DIR_NAME"/bin/activate; then
        echo "Failed to activate virtual environment."
        exit 1
    else
        echo "Virtual environment is active."
    fi
}

function update_pip() {
    echo "Updating pip..."
    if ! "$PIP_EXECUTABLE" install --upgrade pip; then
        echo "Failed to update pip."
        exit 1
    else
        echo "pip is already up to date."
    fi
}

function install_requirements() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Installing packages from $REQUIREMENTS_FILE file..."
        if ! "$PIP_EXECUTABLE" install -r "$REQUIREMENTS_FILE"; then
            echo "Failed to install packages from $REQUIREMENTS_FILE file."
            exit 1
        fi
    else
        echo "$REQUIREMENTS_FILE file not found."
        exit 1
    fi
}

function install_dev_requirements() {
    if [ "$1" == "--dev" ]; then
        if [ -f "$DEV_REQUIREMENTS_FILE" ]; then
            echo "Installing packages from $DEV_REQUIREMENTS_FILE file..."
            if ! "$PIP_EXECUTABLE" install -r "$DEV_REQUIREMENTS_FILE"; then
                echo "Failed to install packages from $DEV_REQUIREMENTS_FILE file."
                exit 1
            fi
        else
            echo "$DEV_REQUIREMENTS_FILE file not found."
            exit 1
        fi
    fi
}

function deactivate_venv() {
    echo "Deactivating virtual environment..."
    deactivate
    echo "Virtual environment is deactivated."
}

function print_python_path() {
    ENV_PYTHON_PATH=$(which "$PYTHON_EXECUTABLE")
    echo ""
    echo "Python path for the $VENV_PROMPT environment:"
    echo " $ENV_PYTHON_PATH"
    echo ""
}

Main script
if [ "$1" != "" ] && [ "$1" != "--dev" ]; then
    usage
fi

check_python
check_venv_module
create_venv
activate_venv
update_pip
install_requirements
install_dev_requirements "$1"
print_python_path
deactivate_venv
