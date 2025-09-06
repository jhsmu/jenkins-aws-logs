pipeline {
    agent any

    stages {

        }

        stage('Install dependencies') {
            steps {
                sh '''
                  python3 -m venv venv
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
                      echo "📌 Usando credencial secreta..."
                      cp "$AWS_ENV_FILE" .env
                      echo "📂 Contenido del .env:"
                      cat .env   # Jenkins enmascarará los valores sensibles
                      
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
