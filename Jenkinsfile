pipeline {
  triggers {
    cron('30 1 * * *')
  }

  agent any

  stages {
    stage('Generate report') {
      agent {
        docker {
            image 'python:3.9.6'
        }
      }
      steps {
        withCredentials([
          usernamePassword(credentialsId: 'illume', usernameVariable: 'ILLUME_USERNAME', passwordVariable: 'ILLUME_PASSWORD'),
          usernamePassword(credentialsId: 'kctcs_ftp', usernameVariable: 'FTP_USERNAME', passwordVariable: 'FTP_PASSWORD')
        ]){
          sh 'python -m venv env && . env/bin/activate && pip install -r requirements.txt && python kctcs_report_basic_auth.py stage illume illume $ILLUME_USERNAME $ILLUME_PASSWORD kctsftpw.mycmsc.com $FTP_USERNAME $FTP_PASSWORD'
        }
      }
    }
    // stage('FTP Upload') {
    //   steps {  
    //     ftpPublisher alwaysPublishFromMaster: true, continueOnError: false, failOnError: false, masterNodeName: '', paramPublish: null, publishers: [
    //         [configName: 'dlptest', transfers: [
    //             [asciiMode: false, cleanRemote: false, excludes: '', flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**.txt']
    //         ], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true]
    //     ]
    //   }
    // }
  }
}
