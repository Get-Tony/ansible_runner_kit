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
REQ_SYSTEM="system.txt"
REQ_MAIN="core.txt"
REQ_DEV="dev.txt"

USE_SYSTEM_PYTHON=false
INSTALL_DEV_PACKAGES=false

check_python_version() {
    echo "Checking Python version..."
    if [ ! -f ./bin/python/check_python_version.py ]; then
        echo "Error: ./bin/python/check_python_version.py not found."
        exit 1
    fi
    $PYTHON_EXECUTABLE ./bin/python/check_python_version.py -v "$1"
}

create_virtual_environment() {
    if ! $PYTHON_EXECUTABLE -m venv --help &>/dev/null; then
        echo "Error: venv module not found."
        echo "Please install the python3-venv package."
        exit 1
    fi
    if [ -f "$1/pyvenv.cfg" ]; then
        VENV_PROMPT_LINE=$(grep -oP '(?<=^prompt\s=\s).*' "$1/pyvenv.cfg")
        if [ "$VENV_PROMPT_LINE" != "'$VENV_PROMPT'" ]; then
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

install_system_requirements() {
    echo "Installing system requirements..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update
        sudo xargs -a "$1" apt-get install -y
    elif command -v yum &>/dev/null; then
        sudo yum update -y
        sudo xargs -a "$1" yum install -y
    else
        echo "Unsupported package manager. Please install: $(xargs -a "$1" echo)"
        exit 1
    fi
}

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

if ! check_python_version "$MINIMUM_PYTHON_VERSION"; then
    exit 1
fi

if ! $USE_SYSTEM_PYTHON; then
    echo "Creating a virtual environment in ${VENV_DIR} directory..."
    create_virtual_environment "${VENV_DIR}"
else
    echo "Using the system Python environment..."
fi

echo "Updating pip..."
$PYTHON_EXECUTABLE -m pip install --upgrade pip

install_system_requirements "${REQUIREMENTS_DIR}/${REQ_SYSTEM}"

install_python_requirements "${REQUIREMENTS_DIR}/${REQ_MAIN}"

if $INSTALL_DEV_PACKAGES; then
    install_python_requirements "${REQUIREMENTS_DIR}/${REQ_DEV}"
fi

if ! $USE_SYSTEM_PYTHON; then
    echo "Setting shebang line of ./ark.py to ./.venv/bin/python..."
    sed -i "1s/.*/#!.venv\/bin\/python/" ./ark.py
    echo ""
else
    echo "Setting shebang line of ./ark.py to /usr/bin/env python..."
    sed -i "1s/.*/#!\/usr\/bin\/env python/" ./ark.py
    echo ""
fi

echo "Done!"
