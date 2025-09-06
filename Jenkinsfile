pipeline {
    agent any

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

        stage('Run with secrets') {
            steps {
                withCredentials([file(credentialsId: 'aws-env-file', variable: 'AWS_ENV_FILE')]) {
                    sh '''
                    echo "📌 Usando credencial secreta..."
                    
                    # ✅ Cargar las variables de entorno de manera segura
                    set -a
                    . "$AWS_ENV_FILE"
                    set +a
                    
                    echo "📂 Las variables de entorno han sido cargadas."
                    
                    # Activar el entorno virtual y ejecutar el script
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
