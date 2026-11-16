pipeline {
    agent any

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONDONTWRITEBYTECODE = '1'
    }

    stages {
        stage('Install') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest -q'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t scms-demo:${BUILD_NUMBER} .'
            }
        }
    }
}
