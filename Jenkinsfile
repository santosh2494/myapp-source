pipeline {
  agent any

  environment {
    REGISTRY = "docker.io/yourdockerhub"
    IMAGE = "myapp"
    VERSION = "${BUILD_NUMBER}"
    GITOPS_REPO = "git@github.com:yourorg/gitops-apps.git"
  }

  stages {

    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Tests') {
      steps { sh 'pytest || true' }
    }

    stage('Build Image') {
      steps {
        script {
          docker.build("${REGISTRY}/${IMAGE}:${VERSION}")
        }
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub-creds',
          usernameVariable: 'USER',
          passwordVariable: 'PASS')]) {

          sh '''
          docker login -u $USER -p $PASS
          docker push ${REGISTRY}/${IMAGE}:${VERSION}
          docker tag ${REGISTRY}/${IMAGE}:${VERSION} ${REGISTRY}/${IMAGE}:latest
          docker push ${REGISTRY}/${IMAGE}:latest
          '''
        }
      }
    }

    stage('Update GitOps') {
      steps {
        sshagent(['gitops-ssh']) {
          sh '''
          git clone ${GITOPS_REPO}
          cd gitops-apps/apps/myapp/overlays/dev
          sed -i "s/newTag:.*/newTag: ${VERSION}/g" kustomization.yaml
          git config user.email "jenkins@company.com"
          git config user.name "jenkins"
          git commit -am "Deploy ${VERSION}"
          git push
          '''
        }
      }
    }
  }
}
