pipeline {
  agent{
        dockerfile {
          filename 'Dockerfile'
        }
      }

  triggers { pollSCM('25 16 * * *') }

  stages {
    stage('docker'){
      steps{
        sh 'python3 -m pytest --alluredir=reports'
      }

    }
  }

  post {
          always{
            allure commandline: 'allure' , results: [[path: 'reports']]
          }
          failure{
              emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at "<a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>"</p>""",
                to: "877649301@qq.com",
                from: "117220100@qq.com"
            )
          }

        }

}