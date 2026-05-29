pipeline {

    agent any

    environment {
        IMAGE_NAME = "santosh2404/myapp"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        GITOPS_REPO = "https://github.com/santosh2494/myapp-source.git"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                url: 'https://github.com/santosh2494/myapp-source.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                    docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Update GitOps Repo') {

            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'gitcreds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {

                    sh '''
                    rm -rf gitops

                    git clone https://$GIT_USER:$GIT_PASS@github.com/YOURUSER/gitops-apps.git gitops

                    cd gitops

                    sed -i "s|image:.*|image: docker.io/santosh2404/myapp:$IMAGE_TAG|g" apps/myapp/base/deployment.yaml

                    git config user.email "jenkins@company.local"
                    git config user.name "Jenkins"

                    git add .
                    git commit -m "Updated image to build $IMAGE_TAG"

                    git push
                    '''
                }
            }
        }
    }
}
