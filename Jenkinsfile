pipeline {
  agent any

  environment {
    AWS_DEFAULT_REGION = 'us-east-1'
    LOG_GROUP          = 'LeancoreInfraStackProd-LeancorePortfolioReporterTask...'
  }

  triggers {
    cron('H/5 * * * *') // cada 5 minutos
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        sh '''
          python3 -m venv venv || true
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run with secret .env') {
      steps {
        withCredentials([file(credentialsId: 'aws-env-file', variable: 'AWS_ENV_FILE')]) {
          sh '''
            echo "Usando credencial secreta..."
            cp "$AWS_ENV_FILE" .env
            . venv/bin/activate
            python export_logs.py
          '''
        }
      }
    }

    stage('Archive logs') {
      steps {
        archiveArtifacts artifacts: 'logs_export.csv', fingerprint: true
      }
    }
  }
}
