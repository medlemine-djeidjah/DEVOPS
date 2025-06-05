# Multi-App Deployment with Jenkins & Ansible

This project demonstrates orchestrating a multi-app deployment (backend, frontend, database) with Jenkins and Ansible, featuring state management and intelligent rollback.

## Project Structure

```
DEVOPS/
├── ansible/
│   ├── playbooks/
│   │   ├── setup_docker.yml    # Installs Docker and Docker Compose on target
│   │   ├── deploy_app.yml      # Deploys applications based on versions.yml
│   │   └── rollback_app.yml    # Rolls back applications to previous versions
│   ├── inventory/
│   │   └── hosts.ini           # Ansible inventory file
│   └── ansible.cfg           # Ansible configuration
├── apps/
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── app.py
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── index.html
│   └── database/
│       └── # We'll likely use a standard image, but a Dockerfile could go here
├── Jenkinsfile                 # Jenkins pipeline script
├── versions.yml                # Defines current and previous versions for deployment
└── README.md
```

## Prerequisites

1.  **VM1 (Jenkins & Ansible Host)**:
    *   Jenkins installed.
    *   Ansible installed.
    *   SSH key (`pops-machine-devops.pem`) for accessing VM2, placed in the Jenkins user's home directory (or accessible by Jenkins).
    *   Git installed.

2.  **VM2 (Application Host)**:
    *   Accessible via SSH from VM1 using the specified key.
    *   Will have Docker and Docker Compose installed by Ansible.

## Setup

### 1. Clone Repository
Clone this repository onto VM1, preferably in a location accessible by Jenkins.

### 2. Configure Ansible
- Update `ansible/inventory/hosts.ini` with the correct IP address or hostname for VM2.
- Ensure `pops-machine-devops.pem` is in the correct path as specified in `ansible.cfg` or SSH config.

### 3. Configure Jenkins
- Create a new Pipeline project in Jenkins.
- Point the pipeline script to the `Jenkinsfile` in this repository.
- Ensure Jenkins has necessary credentials:
    - SSH credentials for VM2 (using the `.pem` key).
    - Git credentials if the repository is private.

## Deployment Process

1.  **Update `versions.yml`**: Modify `versions.yml` with the desired application versions (e.g., image tags).
2.  **Commit and Push**: Commit changes to `versions.yml` (and any application code changes) to the Git repository.
3.  **Trigger Jenkins Job**:
    *   Manually trigger the Jenkins job.
    *   Or, configure a webhook for automatic triggering on Git push.

Jenkins will:
- Checkout the latest code.
- Read `versions.yml`.
- Use Ansible to:
    - Ensure Docker is set up on VM2 (first run).
    - Deploy the specified application versions.

## Rollback
If a deployment fails or a rollback is needed:
- The `deploy_app.yml` playbook can be designed to store the previous `versions.yml` state.
- A separate Jenkins job or parameter can trigger the `rollback_app.yml` playbook, which would use the stored previous versions.

## Application Details

*   **Backend**: A simple Python Flask application.
*   **Frontend**: A basic Nginx server serving static HTML.
*   **Database**: A standard PostgreSQL or MySQL container. 