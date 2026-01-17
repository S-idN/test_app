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
                docker run -d -p 5000:5000 --name community-todo community-todo
                '''
            }
        }
    }
}
