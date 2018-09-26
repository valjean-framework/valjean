def notifyTuleap(boolean success) {
  String statusTag = "failure"
  if (success) {
    statusTag = "success"
  }
  REPO_ID=704  // central repository
  withCredentials([string(credentialsId: "ci-token-${REPO_ID}", variable: 'token')]) {
    sh """
       cd ${SRC}
       rev="\$(git rev-parse HEAD)"
       curl -k "https://codev-tuleap.intra.cea.fr/api/git/${REPO_ID}/statuses/\$rev" \
       -X POST \
       -H 'Content-Type: application/json' \
       -H 'Accept: application/json' \
       --data-binary "{ \\"state\\": \\"$statusTag\\", \\"token\\": \\"$token\\"}"
       """
  }
}

pipeline {
  options {
    skipDefaultCheckout()
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }

  agent { label 'valjean' }

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
        python3 -m pip install --upgrade pip
        python3 -m pip install ${SRC}[dev]
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
    stage('Build and check HTML doc') {
      steps {
        echo 'Building and checking documentation...'
        dir("${SRC}") {
          sh """
             source "${VENV}/bin/activate"
             # be nitpicky on the HTML documentation
             sphinx-build -a -n -b html doc/src doc/build/html |& tee sphinx-html.out
             sphinx-build -a -b linkcheck doc/src doc/build/linkcheck && mv doc/build/linkcheck/output.txt sphinx-linkcheck.out
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
             pytest --cov-report term-missing --cov-config .coveragerc --cov-report=xml --cov=valjean --junit-xml=pytest.xml --timeout=30 | tee pytest.out
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
      warnings(parserConfigurations: [[parserName: 'pep8', pattern: "**/flake8.out"],
                                      [parserName: 'pylint', pattern: "**/pylint.out"],
                                      [parserName: 'sphinx-build', pattern: "**/sphinx-html.out"],
                                      [parserName: 'sphinx-linkcheck', pattern: "**/sphinx-linkcheck.out"]],
               usePreviousBuildAsReference: true)
      archiveArtifacts artifacts: "**/flake8.out", fingerprint: true
      archiveArtifacts artifacts: "**/pylint.out", fingerprint: true
      archiveArtifacts artifacts: "**/sphinx-html.out", fingerprint: true
      archiveArtifacts artifacts: "**/sphinx-linkcheck.out", fingerprint: true
      archiveArtifacts artifacts: "**/pytest.out", fingerprint: true
      junit "**/pytest.xml"
    }
    cleanup {
      cleanWs()
    }
  }
}
