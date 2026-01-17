pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t community-todo .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat '''
                docker stop community-todo || echo Container not running
                docker rm community-todo || echo Container not found
                docker run -d -p 5001:5000 --name community-todo community-todo
                '''
            }
        }

        stage('Expose via ngrok') {
            steps {
                bat '''
                echo Starting ngrok tunnel...
                start /B ngrok http 5001
                '''
            }
        }
    }
}
