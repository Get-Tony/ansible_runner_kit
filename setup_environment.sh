#!/bin/bash

# Constants
MIN_PYTHON_VERSION="3.9.2"
VENV_DIR_NAME=".venv"
VENV_PROMPT="Ansible-Runner"
REQUIREMENTS_FILE="requirements.txt"
DEV_REQUIREMENTS_FILE="requirements.dev.txt"
PYTHON_EXECUTABLE="python3"
PIP_EXECUTABLE="pip"

# Usage
function usage() {
    echo "Usage: $0 [--dev]"
    echo "This script will create a virtual environment and install packages from the requirements.txt file."
    echo "If the --dev argument is passed, it will also install packages from the requirements.dev.txt file."
    echo "If the virtual environment already exists, it will exit."
    exit 1
}

# If any argument other then --dev is passed, print usage and exit
if [ "$1" != "" ] && [ "$1" != "--dev" ]; then
    echo "Usage: $0 [--dev]"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v "$PYTHON_EXECUTABLE" &>/dev/null; then
    echo "$PYTHON_EXECUTABLE is not installed. Please install $PYTHON_EXECUTABLE $MIN_PYTHON_VERSION or later."
    exit 1
fi

# Get the version of Python 3
PYTHON_VERSION=$("$PYTHON_EXECUTABLE" -V 2>&1 | awk '{print $2}')

# Check if Python 3 version is at least the minimum required version
if [ "$(printf '%s\n' "$MIN_PYTHON_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_PYTHON_VERSION" ]; then
    echo "$PYTHON_EXECUTABLE version is too old. Please upgrade to $PYTHON_EXECUTABLE $MIN_PYTHON_VERSION or later."
    exit 1
fi

echo "$PYTHON_EXECUTABLE $MIN_PYTHON_VERSION or later is installed."

# Check if venv module is available
if ! "$PYTHON_EXECUTABLE" -c 'import venv' &>/dev/null; then
    echo "venv module is not available. Please install it and try again."
    exit 1
fi

echo "venv module is available."

# Check if .venv directory exists
if [ ! -d "$VENV_DIR_NAME" ]; then
    echo "Creating virtual environment..."
    if ! "$PYTHON_EXECUTABLE" -m venv "$VENV_DIR_NAME" --prompt "$VENV_PROMPT"; then
        echo "Failed to create virtual environment."
        exit 1
    fi
else
    echo "Virtual environment directory already exists."
    echo "If you want to create a new virtual environment, please delete the $VENV_DIR_NAME directory and try again."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
if ! source "$VENV_DIR_NAME"/bin/activate; then
    echo "Failed to activate virtual environment."
    exit 1
else
    echo "Virtual environment is active."
fi

# Update pip
echo "Updating pip..."
if ! "$PIP_EXECUTABLE" install --upgrade pip; then
    echo "Failed to update pip."
    exit 1
else
    echo "pip is already up to date."
fi

# Install packages from requirements.txt file
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing packages from $REQUIREMENTS_FILE file..."
    if ! "$PIP_EXECUTABLE" install -r "$REQUIREMENTS_FILE"; then
        echo "Failed to install packages from $REQUIREMENTS_FILE file."
        exit 1
    fi
else
    echo "$REQUIREMENTS_FILE file not found."
fi

# Check if --dev argument is passed and install packages from requirements.dev.txt file
if [ "$1" == "--dev" ]; then
    if [ -f "$DEV_REQUIREMENTS_FILE" ]; then
        echo "Installing packages from $DEV_REQUIREMENTS_FILE file..."
        if ! "$PIP_EXECUTABLE" install -r "$DEV_REQUIREMENTS_FILE"; then
            echo "Failed to install packages from $DEV_REQUIREMENTS_FILE file."
            exit 1
        fi
    else
        echo "$DEV_REQUIREMENTS_FILE file not found."
    fi
fi

# Get path to Python 3 in virtual environment
ENV_PYTHON_PATH=$(which "$PYTHON_EXECUTABLE")

# Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate

# Print path to Python 3 for the virtual environment
echo ""
echo "Python path for the $VENV_PROMPT environment:"
echo "    $ENV_PYTHON_PATH"
echo ""
