pipeline {
    agent any

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONDONTWRITEBYTECODE = '1'
    }

    stages {
        stage('Install & Test') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$WORKSPACE:/app" \
                        -w /app \
                        python:3.12-slim \
                        sh -c "pip install -r requirements.txt && python -m pytest -v"
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t scms-demo:${BUILD_NUMBER} .'
            }
        }
    }
}