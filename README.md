# Ansible Runner Kit (ARK)

The Ansible Runner Kit (ARK) is a command-line interface (CLI) tool designed to help manage and execute Ansible playbooks, work with inventory, and manage cron jobs related to Ansible tasks. This repository contains the following files:

- setup.sh - A script to set up the environment for the project.
- ark.py - The main CLI script for the Ansible Runner Kit.

## Getting Started

### Prerequisites

Ensure you have Python 3.9.2 or higher installed on your system. You can check your Python version by running:

    python3 --version

### Setting Up the Development Environment

To set up the development environment, run the setup.sh script. This script creates a virtual environment, installs the required Python packages, and sets up any necessary system packages.

    ./setup.sh

By default, the script creates a virtual environment. If you prefer to use the system Python environment instead, run the script with the --system flag:

    ./setup.sh --system

To install development packages, use the --dev flag:

    ./setup.sh --dev

After setting up the environment, activate the virtual environment (if you didn't use the --system flag) by running:

    source .venv/bin/activate

### Using the Ansible Runner Kit (ARK)

Create a new `env/ssh_key` file and add your SSH private key to it. This file will be used to connect to remote hosts.

- **Ensure the SSH key file is not publicly accessible.**

- **If you are using `git`, ensure the `ssh_key` file is in your `.gitignore` file.**

Example `.gitignore` entry:

    **/ssh_key

To start using ARK, run the ark script with the desired command and options.

Ensure you are in the project directory before running the script.

Make ARK executable:

    chmod +x ark

List available playbooks:

    ./ark run

For detailed information about ARK commands and options, refer to the ARK Command Summary.

## ARK Command Summary

- run - Executes an Ansible playbook in the project.
- lint - Lints an Ansible playbook using ansible-lint.
- report - Displays Ansible run report(s).
- inv - Inventory-related commands.
  - get_host_groups - Displays all groups a host is a member of.
  - get_group_hosts - Displays all hosts in a group.
- cron - Manages cron jobs related to Ansible tasks.
  - create - Creates a cron job.
  - delete - Deletes a cron job.
  - list - Lists all ARK cron jobs for a user.

For detailed information about ARK commands and options, refer to the ARK Help.

    `./ark --help`

## Customizing the Environment

- The `project` directory contains the main playbook file `main.yml` and the roles directory.

- New [Ansible Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html) can be added to the `project` directory.

- New [Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) can be added to the `project/roles` directory.

- To run a different playbook, the playbook name must be passed as an argument to the `ark.py` script.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch with your changes.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Ansible](https://www.ansible.com/)
- [Ansible-runner](https://ansible-runner.readthedocs.io/en/latest/)
- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)

- ARK Author: [Get-Tony](https://github.com/Get-Tony)
