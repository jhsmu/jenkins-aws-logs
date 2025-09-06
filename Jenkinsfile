pipeline {
    agent any

    environment {
        // 🔑 Variables cargadas desde Jenkins Credentials
        AWS_ACCESS_KEY_ID     = credentials('e14fc09e-c936-4630-8c3f-4b8fb76c87d52')
        AWS_SECRET_ACCESS_KEY = credentials('e03832c5-e0f4-415f-8fc8-133a95a9e996')
        AWS_DEFAULT_REGION    = 'us-east-1'
        LOG_GROUP             = 'LeancoreInfraStackProd-LeancorePortfolioReporterTaskleancoreportfolioreporterLogGroupD62FBEF1-V5zAjptjzyox'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Jemena12/jenkins-aws-logs.git'
            }
        }

        stage('Instalar dependencias') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Ejecutar script') {
            steps {
                sh './venv/bin/python export_logs.py'
            }
        }

        stage('Guardar artefactos') {
            steps {
                archiveArtifacts artifacts: 'logs_export.csv', fingerprint: true
            }
        }
    }
}
