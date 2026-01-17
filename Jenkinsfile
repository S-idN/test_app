pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t community-todo .'
            }
        }

        stage('Start Redis') {
            steps {
                bat '''
                docker stop redis || echo Redis not running
                docker rm redis || echo Redis not found
                docker run -d --name redis redis:7-alpine
                '''
            }
        }

        stage('Deploy App Container') {
            steps {
                bat '''
                docker stop community-todo || echo App not running
                docker rm community-todo || echo App not found
                docker run -d ^
                  --name community-todo ^
                  --link redis ^
                  -p 5001:5000 ^
                  community-todo
                '''
            }
        }
    }
}
