#!/bin/bash
# This script is used to setup the development environment for the project.
# It creates a virtual environment and installs all the required packages.
# It also installs system packages required by the project.
# Usage:
#   ./setup.sh [--system] [--dev]
#   --system: Use the system Python environment instead of creating a virtual environment.
#   --dev: Install development packages.
# Author:
#   Anthony Pagan (GitHub: @Get-Tony)

set -e

PYTHON_EXECUTABLE="python3"
VENV_PROMPT="ARK Env"
REQUIREMENTS_DIR="./requirements"
VENV_DIR="./.venv"
MINIMUM_PYTHON_VERSION="3.9.2"
REQ_MAIN="core.txt"
REQ_DEV="dev.txt"

USE_SYSTEM_PYTHON=false
INSTALL_DEV_PACKAGES=false

check_required_files_and_folders() {
    local missing_files_or_folders=false
    local required_files_or_folders=(
        "$REQUIREMENTS_DIR"
        "$REQUIREMENTS_DIR/$REQ_MAIN"
        "$REQUIREMENTS_DIR/$REQ_DEV"
        "./bin/check_python_version.py"
    )
    for file_or_folder in "${required_files_or_folders[@]}"; do
        if [ ! -e "$file_or_folder" ]; then
            echo "Error: $file_or_folder not found."
            missing_files_or_folders=true
        fi
    done
    if $missing_files_or_folders; then
        echo "Please make sure all required files and folders are present before running the script."
        exit 1
    fi
}

check_python_version() {
    echo "Checking Python version..."
    if [ ! -f ./bin/check_python_version.py ]; then
        echo "Error: ./bin/check_python_version.py not found."
        exit 1
    fi
    $PYTHON_EXECUTABLE ./bin/check_python_version.py -v "$1"
}

create_virtual_environment() {
    if ! $PYTHON_EXECUTABLE -m venv --help &>/dev/null; then
        echo "Error: venv module not found."
        echo "Please install the python3-venv package."
        exit 1
    fi
    if [ -f "$1/pyvenv.cfg" ]; then
        VENV_PROMPT_LINE=$(grep -oP '(?<=^prompt\s=\s).*' "$1/pyvenv.cfg")
        if [ "$VENV_PROMPT_LINE" != "$VENV_PROMPT" ]; then
            echo "A virtual environment directory already exists with an unrecognized prompt."
            echo "Please delete or move the $1 directory and try again."
            exit 1
        fi
        echo "Using existing virtual environment..."
    else
        echo "Creating virtual environment..."
        $PYTHON_EXECUTABLE -m venv "$1" --prompt "$VENV_PROMPT"
    fi
    source "$1/bin/activate"
}

install_python_requirements() {
    echo "Installing Python requirements from $1..."
    $PYTHON_EXECUTABLE -m pip install -r "$1"
}

## Main loop

# Check for required files and folders
check_required_files_and_folders

# Check if python3 and python3-venv are installed
if ! command -v $PYTHON_EXECUTABLE &>/dev/null; then
    echo "Error: python3 not found."
    echo "Please install python3 and python3-venv before running this script."
    exit 1
elif ! $PYTHON_EXECUTABLE -c "import venv" &>/dev/null; then
    echo "Error: python3-venv not found."
    echo "Please install python3-venv before running this script."
    exit 1
fi

# Parse arguments
for arg in "$@"; do
    case $arg in
    --system)
        USE_SYSTEM_PYTHON=true
        ;;
    --dev)
        INSTALL_DEV_PACKAGES=true
        ;;
    esac
done

# Check Python version
if ! check_python_version "$MINIMUM_PYTHON_VERSION"; then
    exit 1
fi

# Check for system flag else create virtual environment
if ! $USE_SYSTEM_PYTHON; then
    echo "Creating a virtual environment in ${VENV_DIR} directory..."
    create_virtual_environment "${VENV_DIR}"
else
    echo "Using the system Python environment..."
fi

echo "Installing Ansible-Runner Kit..."

# Install or upgrade pip
echo "Updating pip..."
$PYTHON_EXECUTABLE -m pip install --upgrade pip

# Install Python requirements
install_python_requirements "${REQUIREMENTS_DIR}/${REQ_MAIN}"

# Install Python development requirements
if $INSTALL_DEV_PACKAGES; then
    install_python_requirements "${REQUIREMENTS_DIR}/${REQ_DEV}"
fi

echo ""
echo "Ansible-Runner Kit setup complete."
echo ""
