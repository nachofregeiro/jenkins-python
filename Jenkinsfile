pipeline {
  agent any

  stages {
    stage('Run') {
      agent {
        docker {
            image 'python:3.5.1'
        }
      }
      steps {
        script {
          sh 'python -m venv env && source ./env/bin/activate && pip install -r requirements.txt && python print.py'
        }
      }
    }
    stage('Upload') {
      steps {  
        ftpPublisher alwaysPublishFromMaster: true, continueOnError: false, failOnError: false, masterNodeName: '', paramPublish: null, publishers: [
            [configName: 'dlptest', transfers: [
                [asciiMode: false, cleanRemote: false, excludes: '', flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**.txt']
            ], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true]
        ]
      }
    }
  }
}
