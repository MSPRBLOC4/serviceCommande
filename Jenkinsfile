pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DATABASE_URL="postgresql://postgres:root@postgres:5432/mspr2"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/MSPRBLOC4/serviceCommande.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
                sh './venv/bin/pip install pytest-cov'

            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    export DATABASE_URL="sqlite:///./test.db"
                    export PYTHONPATH=$(pwd)
                    ./venv/bin/pytest --cov=. tests/ --cov-report=xml
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh''cd docker'
                    sh 'docker build -t mspr2 .'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Déploiement à venir...'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
    }
}

