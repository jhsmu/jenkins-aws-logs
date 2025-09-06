pipeline {
    agent any

    environment {
        // Las variables se cargan desde los secretos de Jenkins
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')     // Secret Text
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY') // Secret Text
        AWS_DEFAULT_REGION    = credentials('AWS_DEFAULT_REGION')    // Secret Text, ej: us-east-1
        LOG_GROUP             = credentials('LOG_GROUP')         // Secret Text, ej: LeancoreInfraStackProd-...
    }

    stages {
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

        stage('Run export_logs.py') {
            steps {
                sh '''
                  echo "📌 Variables de entorno cargadas desde Jenkins Secret Text"

                  # Activar entorno virtual y ejecutar script
                  . venv/bin/activate
                  python export_logs.py
                '''
            }
        }

        stage('Archive logs') {
            steps {
                archiveArtifacts artifacts: 'logs_export.csv', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Exportación de logs completada"
        }
        failure {
            echo "❌ Hubo un error en la exportación de logs"
        }
    }
}
