def notifyTuleap(boolean success) {
  String statusTag = "F"
  if (success) {
    statusTag = "S"
  }
  def git_url = sh([script: "cd ${SRC} && git config remote.origin.url", returnStdout: true]).trim()
  if (git_url.contains("dm232107")) {
    REPO_ID=705  // DM's sandbox
  } else if (git_url.contains("el220326")) {
    REPO_ID=712  // ELM's sandbox
  } else {
    REPO_ID=704  // central repository
  }
  
  echo "Associating ${git_url} to Tuleap repository ID ${REPO_ID}"
  withCredentials([string(credentialsId: "ci-token-${REPO_ID}", variable: 'token')]) {
    sh """
       cd ${SRC}
       rev="\$(git rev-parse HEAD)"
       curl -k "https://codev-tuleap.intra.cea.fr/api/git/${REPO_ID}/build_status" \
       -H 'Content-Type: application/json' \
       -H 'Accept: application/json' \
       --data-binary "{ \\"status\\": \\"$statusTag\\", \\"branch\\": \\"\$BRANCH_NAME\\", \\"commit_reference\\": \\"\$rev\\", \\"token\\": \\"$token\\"}"
       """
  }
}

pipeline {
  options {
    skipDefaultCheckout()
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }

  agent any

  environment {
    projectName = 'valjean'
    SRC = "${env.WORKSPACE}/src"
    VENV = "${env.WORKSPACE}/venv"
  }

  stages {
    stage('Checkout') {
      steps {
        dir("${SRC}") {
          checkout scm
        }
      }
    }
    stage('Install') {
      steps {
        echo "Starting build ${env.BUILD_ID} on ${env.JENKINS_URL}..."
        sh """
        python3 -m venv "${VENV}"
        source "${VENV}/bin/activate"
        pip install --upgrade pip
        pip install ${SRC}[dev]
        """
      }
    }
    stage('Linting') {
      steps {
        echo 'Linting...'
        dir("${SRC}") {
          sh """
              source "${VENV}/bin/activate"
              pylint -f parseable valjean/ tests/ | tee pylint.out
              # flake8 returns 1 in case of warnings and that would stop the
              # build
              flake8 --tee --output-file flake8.out || true
              # avoid empty flake8.out files, Jenkins complains 
              echo "end of flake8 file" >> flake8.out
              """
        }
      }
    }
    stage('Build HTML doc') {
      steps {
        echo 'Building documentation...'
        dir("${SRC}") {
          sh """
             source "${VENV}/bin/activate"
             sphinx-build -b html doc/src doc/build/html | tee sphinx.out
             """
        }
      }
    }
    stage('Run doctests') {
      steps {
        echo 'Running doctests...'
          dir("${SRC}/doc") {
            sh """
               source "${VENV}/bin/activate"
               sphinx-build -b doctest src build/doctest | tee doctest.out
               """
          }
      }
    }
    stage('Run unit tests') {
      steps {
        echo 'Running unit tests...'
        dir("${SRC}") {
          sh """
             source "${VENV}/bin/activate"
             pytest --cov-report=xml --cov=valjean --junit-xml=pytest.xml | tee pytest.out
             readlink -f pytest.xml tests/coverage.xml
             """
          step([$class: 'CoberturaPublisher',
                autoUpdateHealth: false,
                autoUpdateStability: false,
                coberturaReportFile: 'tests/coverage.xml',
                failUnhealthy: false,
                failUnstable: false,
                maxNumberOfBuilds: 0,
                onlyStable: false,
                sourceEncoding: 'ASCII',
                zoomCoverageChart: false])
        }
      }
    }
  }
  post {
    success {
        notifyTuleap(true)
    }
    failure {
        notifyTuleap(false)
    }
    always {
      warnings parserConfigurations: [[parserName: 'flake8', pattern: "flake8.out"], [parserName: 'pylint', pattern: "pylint.out"]], usePreviousBuildAsReference: true
      archiveArtifacts artifacts: "**/pylint.out", fingerprint: true
      archiveArtifacts artifacts: "**/flake8.out", fingerprint: true
      archiveArtifacts artifacts: "**/pytest.out", fingerprint: true
      archiveArtifacts artifacts: "**/doctest.out", fingerprint: true
      archiveArtifacts artifacts: "**/sphinx.out", fingerprint: true
      junit "**/pytest.xml"
    }
    cleanup {
      cleanWs()
    }
  }
}
