pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "docker.io/library/devops-assignment-2"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        SONARQUBE_SERVER = "SonarQubeServer"
    }

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run pytest') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest -v --junitxml=pytest-report.xml
                '''
            }
        }

        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh '''
                        . .venv/bin/activate
                        sonar-scanner
                    '''
                }
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest .'
            }
        }

        stage('Push Docker image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    sh '''
                        echo "${DOCKERHUB_PASSWORD}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'pytest-report.xml'
            cleanWs()
        }
    }
}
