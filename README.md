# Ansible Runner Kit (ARK)

The Ansible Runner Kit (ARK) is a command-line interface (CLI) tool designed to help manage and execute Ansible playbooks, work with inventory, and manage cron jobs for established Ansible Playbooks.

## Getting Started

### Table of Contents

- [Ansible Runner Kit (ARK)](#ansible-runner-kit-ark)
  - [Getting Started](#getting-started)
    - [Table of Contents](#table-of-contents)
    - [Prerequisites](#prerequisites)
    - [Setting Up the Development Environment](#setting-up-the-development-environment)
  - [Using the Ansible Runner Kit (ARK)](#using-the-ansible-runner-kit-ark)
    - [SSH Configuration](#ssh-configuration)
    - [Running ARK](#running-ark)
    - [ARK Command Reference](#ark-command-reference)
      - [Basic Commands](#basic-commands)
  - [Customizing the Environment](#customizing-the-environment)
    - [Ansible Settings](#ansible-settings)
  - [Code of Conduct](#code-of-conduct)
  - [Security](#security)
  - [Contributing](#contributing)
  - [License](#license)
  - [Under the Hood](#under-the-hood)

### Prerequisites

Ensure you have Python 3.9.2 or higher installed on your system. You can check your Python version by running:

    python3 --version

### Setting Up the Development Environment

To set up the development environment, run the setup.sh script. This script creates a virtual environment, installs the required Python packages, and sets up any necessary system packages.

    ./setup.sh

By default, the script creates a virtual environment. If you prefer to use the system Python environment instead, run the script with the `--system` flag:

    ./setup.sh --system

To install development packages, use the `--dev` flag:

    ./setup.sh --dev

After setting up the environment, activate the virtual environment (if you didn't use the `--system` flag) by running:

    source .venv/bin/activate

## Using the Ansible Runner Kit (ARK)

### SSH Configuration

Create a new `env/ssh_key` file and add your SSH private key to it. This file will be used to connect to remote hosts.

- **Ensure the SSH key file is not publicly accessible.**

- **If you are using version control, ensure the `ssh_key` and any other sensitive files are excluded using the `.gitignore` file.**

Example `.gitignore` entry to exclude the `ssh_key` file:

    **/ssh_key

### Running ARK

To start using ARK, run the ark script with the desired command and options.

Ensure you are in the project directory before running the script.

Make ARK executable:

    chmod +x ark

List available playbooks:

    ./ark run

### ARK Command Reference

For most commands, you can use the `--help` option to display detailed information about the command and its options.

The `--user` option will normally default to the current user. If you are running ARK as a different user, you can specify the user with the `--user` option.

#### Basic Commands

- `help` - Displays ARK help.

- `run` - Executes an Ansible playbook in the project.
- `lint` - Lints an Ansible playbook using ansible-lint.
- `report` - Displays Ansible run report(s).
- `inv` - Inventory-related commands.
  - `get_host_groups` - Displays all groups a host is a member of.
  - `get_group_hosts` - Displays all hosts in a group.
- `cron` - Manages cron jobs related to Ansible tasks.
  - `create` - Creates a cron job.
  - `delete` - Deletes a cron job.
  - `list` - Lists all ARK cron jobs for a user.

**For detailed information about ARK commands and options, refer to the ARK Help.**

    `./ark --help`

## Customizing the Environment

- The `project` directory contains the main playbook file `main.yml` and the roles directory.

- New [Ansible Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html) can be added to the `project` directory.

- New [Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) can be added to the `project/roles` directory.

- To run a different playbook, the playbook name must be passed as an argument to the `ark.py` script.

### Ansible Settings

Ansible settings can be customized by adding or removing Ansible environment variables in the `env/envvars` file.

Refer to the [Ansible Configuration Settings](https://docs.ansible.com/ansible/latest/reference_appendices/config.html) for more options and information.

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [Get-Tony](https://github.com/Get-Tony).

## Security

If you discover a security vulnerability within this project, please submit a report to [Issues](https://github.com/Get-Tony/ansible_runner_kit/issues/new/choose). All security vulnerabilities will be addressed as soon as possible.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Under the Hood

- [Ansible](https://www.ansible.com/)
- [Ansible-runner](https://ansible-runner.readthedocs.io/en/latest/)
- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)

---

[Back to top](#ansible-runner-kit-ark)
