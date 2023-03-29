#!/bin/bash
# ./create_ansible_collection.sh <namespace> <collection_name> <local_git_server_url>

# Check for the correct number of arguments
if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <namespace> <collection_name> <your_local_git_server_url>"
    exit 1
fi

# Assign input variables from command-line arguments
NAMESPACE="$1"
COLLECTION_NAME="$2"
YOUR_LOCAL_GIT_SERVER_URL="$3"

# Install Ansible
if ! sudo apt update || ! sudo apt install -y ansible; then
    echo "Failed to install Ansible. Please try again."
    exit 1
fi

# Create Ansible collection
if ! ansible-galaxy collection init "${NAMESPACE}.${COLLECTION_NAME}"; then
    echo "Failed to create Ansible collection. Please try again."
    exit 1
fi

# Change to collection directory
cd "${NAMESPACE}.${COLLECTION_NAME}" || {
    echo "Failed to change directory. Please try again."
    exit 1
}

# Add roles, plugins, and modules to the collection directory structure here

# Build the collection
if ! ansible-galaxy collection build; then
    echo "Failed to build Ansible collection. Please try again."
    exit 1
fi

# Initialize a Git repository
if ! git init; then
    echo "Failed to initialize Git repository. Please try again."
    exit 1
fi

# Add and commit files
if ! git add . || ! git commit -m "Initial commit of ${NAMESPACE}.${COLLECTION_NAME} collection"; then
    echo "Failed to add and commit files to Git repository. Please try again."
    exit 1
fi

# Add the local Git server as a remote repository
if ! git remote add origin "${YOUR_LOCAL_GIT_SERVER_URL}/${NAMESPACE}/${COLLECTION_NAME}.git"; then
    echo "Failed to add the local Git server as a remote repository. Please try again."
    exit 1
fi

# Push the collection to the local Git server
if ! git push -u origin master; then
    echo "Failed to push the collection to the local Git server. Please try again."
    exit 1
fi

# Create a requirements.yml file
cat <<EOF >requirements.yml
---
collections:
  - name: ${YOUR_LOCAL_GIT_SERVER_URL}/${NAMESPACE}/${COLLECTION_NAME}.git
    type: git
    version: master
EOF

echo "Ansible collection created and pushed to the local Git server. Share the repository URL and requirements.yml file with the target machines in the air-gapped network."
