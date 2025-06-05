pipeline {
    agent any // Runs on any available agent. You might restrict this to VM1 if needed.

    environment {
        // Path to Ansible playbooks relative to the workspace root
        ANSIBLE_PLAYBOOKS_PATH = "ansible/playbooks"
        // SSH Credential ID for VM2 stored in Jenkins
        // Replace 'vm2-ssh-creds' with your actual Jenkins credential ID for the .pem file
        VM2_SSH_CREDENTIAL_ID = 'vm2-ssh-creds' 
    }

    parameters {
        booleanParam(name: 'PERFORM_ROLLBACK', defaultValue: false, description: 'Trigger a rollback to the previous version?')
        booleanParam(name: 'RUN_DOCKER_SETUP', defaultValue: false, description: 'Run Docker setup on VM2? (Usually only needed once or on new VMs)')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code...'
                checkout scm
                // Ensure versions.yml is present
                sh 'ls -l versions.yml'
            }
        }

        stage('Setup Docker on VM2 (Conditional)') {
            when {
                expression { params.RUN_DOCKER_SETUP == true }
            }
            steps {
                echo 'Running Docker setup on VM2...'
                // Ansible playbook execution for Docker setup
                // Jenkins needs to be able to find ansible-playbook
                // and have access to the private key specified in ansible.cfg
                // The sshAgent wrapper injects the specified credentials for SSH auth
                sshagent([VM2_SSH_CREDENTIAL_ID]) {
                    sh """
                        ansible-playbook -i ansible/inventory/hosts.ini ${ANSIBLE_PLAYBOOKS_PATH}/setup_docker.yml
                    """
                }
            }
        }

        stage('Deploy Applications') {
            when {
                expression { params.PERFORM_ROLLBACK == false }
            }
            steps {
                echo 'Deploying applications to VM2...'
                sshagent([VM2_SSH_CREDENTIAL_ID]) {
                    sh """
                        ansible-playbook -i ansible/inventory/hosts.ini ${ANSIBLE_PLAYBOOKS_PATH}/deploy_app.yml 
                    """
                    // Example of how to pass extra vars if needed:
                    // ansible-playbook -i ansible/inventory/hosts.ini ${ANSIBLE_PLAYBOOKS_PATH}/deploy_app.yml --extra-vars \"frontend_image_repo=mycustomrepo/frontend backend_image_repo=mycustomrepo/backend\"
                }
                echo 'Deployment attempt finished.'
            }
        }

        stage('Rollback Applications (Conditional)') {
            when {
                expression { params.PERFORM_ROLLBACK == true }
            }
            steps {
                echo 'Rolling back applications on VM2 to previous version...'
                sshagent([VM2_SSH_CREDENTIAL_ID]) {
                    sh """
                        ansible-playbook -i ansible/inventory/hosts.ini ${ANSIBLE_PLAYBOOKS_PATH}/rollback_app.yml
                    """
                }
                echo 'Rollback attempt finished.'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            // Clean up workspace or other actions if needed
            // cleanWs()
        }
        success {
            echo 'Pipeline executed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
            // Add notification steps here (e.g., email, Slack)
        }
    }
} 