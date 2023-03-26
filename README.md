
# Ansible Runner Kit (ARK)

ARK provides a set of tools to define an [Ansible-runner](https://ansible-runner.readthedocs.io/en/latest/) environment and workflow.

- [Ansible Runner Kit (ARK)](#ansible-runner-kit-ark)
  - [Project Structure](#project-structure)
    - [artifacts](#artifacts)
    - [env](#env)
      - [env/ssh\_key](#envssh_key)
      - [env/envvars](#envenvvars)
    - [inventory](#inventory)
    - [project](#project)
      - [roles](#roles)
  - [Other files](#other-files)
  - [Requirements](#requirements)
    - [Python](#python)
    - [Operating System](#operating-system)
  - [Usage](#usage)
    - [Setup](#setup)
    - [Running a Playbook](#running-a-playbook)
    - [Customizing the Environment](#customizing-the-environment)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Project Structure

The project directory structure looks like this:

        ansible_runner_kit
        ├── artifacts
        ├── env
        │   ├── envvars
        │   └── ssh_key
        ├── .gitignore
        ├── inventory
        │   └── <Ansible-Inventory>
        ├── project
        │   ├── main.yml
        │   └── roles
        │       └── <Ansible-Roles>
        ├── README.md
        ├── requirements.dev.txt
        ├── requirements.txt
        ├── ark.py
        └── setup_environment.sh

### artifacts

The artifacts directory is used by Ansible-runner to store artifacts from previous runs of the playbook. The ansible fact cache, the playbook output, and the playbook status are stored in this directory.

### env

#### env/ssh_key

The ssh_key directory contains the SSH key used by Ansible-runner to connect to the managed hosts.

#### env/envvars

The envvars file contains environment variables that are used by Ansible-runner.

### inventory

The inventory directory contains the inventory files for Ansible.

- More information: [Ansible Inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)

### project

The project directory contains the main playbook file `main.yml` and the roles directory.

#### roles

The roles directory contains the roles used by the playbooks.

- More information: [Ansible Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)

## Other files

- **.gitignore:** Used to exclude files or directories from Git. SSH keys and other sensitive data must be included. More information can be found at [git-scm](https://git-scm.com/docs/gitignore).
- **requirements.txt:** The Python packages required to run the Ansible playbook.
- **requirements.dev.txt:** Additional Python packages required for development.
- **ark.py:** Runs the named playbook, from the project directory, using Ansible-runner. Limits the artifacts to the last 7 runs.
- **setup_environment.sh:** Creates a virtual environment and install the required Python packages.

## Requirements

### Python

- [Python 3.9+](https://www.python.org/downloads/)

### Operating System

The Ansible-runner environment was built on [Debian 11](https://www.debian.org/releases/bullseye/). It should work on other Linux distributions as well.

## Usage

### Setup

The following command will create a virtual environment and install the required Python packages.

If the `--dev` argument is included, it will also install packages from the development requirements.

If the virtual environment already exists, the script will exit.

To set up the ansible-runner environment, run:

        source setup_environment.sh [--dev]

### Running a Playbook

The `ark.py` script is used to run the Ansible playbook using Ansible-runner.

The script takes one argument, which is the name of the playbook file to be run. If no argument is provided, the script will run the playbook `main.yml`.

To run the playbook `project/main.yml` explicitly, run:

        ./ark.py main.yml

### Customizing the Environment

- The `project` directory contains the main playbook file `main.yml` and the roles directory.

- New [Ansible Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html) can be added to the `project` directory.

- New [Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) can be added to the `project/roles` directory.

- To run a different playbook, the playbook name must be passed as an argument to the `ark.py` script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Ansible](https://www.ansible.com/)
- [Ansible-runner](https://ansible-runner.readthedocs.io/en/latest/)
- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)

---
[Back To Top](#ansible-runner-kit-ark)
