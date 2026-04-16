pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
        timeout(time: 90, unit: 'MINUTES')
        ansiColor('xterm')
    }

    parameters {
        choice(
            name: 'TEST_SCOPE',
            choices: ['smoke', 'marker', 'full'],
            description: 'Execution mode: smoke (fast sanity), marker (one category), full (complete regression).'
        )
        choice(
            name: 'PYTEST_MARKER',
            choices: ['reports', 'metro_areas', 'custom_dashboards', 'accounts', 'contacts', 'documents', 'transactions'],
            description: 'Category to run when TEST_SCOPE=marker. Ignored for smoke/full.'
        )
        booleanParam(
            name: 'RUN_ALLURE',
            defaultValue: true,
            description: 'Publish Allure report in Jenkins (requires Allure plugin installed).'
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: true,
            description: 'Send HTML email summary when pipeline finishes.'
        )
        string(
            name: 'ADDITIONAL_EMAILS',
            defaultValue: '',
            description: 'Optional extra recipients (comma-separated). Example: qa@company.com, manager@company.com'
        )
        string(
            name: 'DEFAULT_EMAIL',
            defaultValue: 'usman.arshad@rolustech.com',
            description: 'Primary email recipient for build notifications.'
        )
        string(
            name: 'SF_CREDENTIALS_ID',
            defaultValue: 'sf-marketplace-creds',
            description: 'Jenkins Username/Password credential ID used for Salesforce login.'
        )
    }

    environment {
        VENV_DIR = '.venv-jenkins'
        PYTEST_JUNIT = 'test-results/pytest.xml'
        PYTEST_HTML = 'test-results/report.html'
        PYTEST_JSON = 'test-results/report.json'
        ALLURE_DIR = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    def shortCommit = env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : 'N/A'
                    echo "Branch: ${env.BRANCH_NAME ?: 'main'} | Commit: ${shortCommit}"
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv ${VENV_DIR}
                            . ${VENV_DIR}/bin/activate
                            python -m pip install --upgrade pip
                            pip install -r salesforce_tab_performance/requirements.txt
                            pip install pytest-html pytest-json-report
                        '''
                    } else {
                        bat '''
                            py -m venv %VENV_DIR%
                            call %VENV_DIR%\\Scripts\\activate
                            python -m pip install --upgrade pip
                            pip install -r salesforce_tab_performance/requirements.txt
                            pip install pytest-html pytest-json-report
                        '''
                    }
                }
            }
        }

        stage('Prepare Report Directories') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            rm -rf test-results allure-results || true
                            mkdir -p test-results allure-results
                        '''
                    } else {
                        bat '''
                            if exist test-results rmdir /s /q test-results
                            if exist allure-results rmdir /s /q allure-results
                            mkdir test-results
                            mkdir allure-results
                        '''
                    }
                }
            }
        }

        stage('Static Validation') {
            steps {
                script {
                    if (params.TEST_SCOPE == 'marker') {
                        echo "Marker mode selected -> running marker: ${params.PYTEST_MARKER}"
                    } else {
                        echo "Scope selected -> ${params.TEST_SCOPE} (marker parameter ignored)"
                    }
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            pytest --version
                            pytest --markers
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate
                            pytest --version
                            pytest --markers
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def runCmd = buildPytestCommand(params.TEST_SCOPE as String, params.PYTEST_MARKER as String, params.RUN_ALLURE as boolean)
                    echo "Pytest command: ${runCmd}"

                    withCredentials([usernamePassword(
                        credentialsId: "${params.SF_CREDENTIALS_ID}",
                        usernameVariable: 'SF_USERNAME',
                        passwordVariable: 'SF_PASSWORD'
                    )]) {
                        if (isUnix()) {
                            sh """
                                . ${VENV_DIR}/bin/activate
                                ${runCmd}
                            """
                        } else {
                            bat """
                                call %VENV_DIR%\\Scripts\\activate
                                ${runCmd}
                            """
                        }
                    }
                }
            }
        }

        stage('Publish Reports') {
            steps {
                script {
                    if (fileExists(env.PYTEST_JUNIT)) {
                        junit testResults: env.PYTEST_JUNIT, allowEmptyResults: true
                    }

                    publishHTML(target: [
                        reportName: 'Pytest HTML Report',
                        reportDir: 'test-results',
                        reportFiles: 'report.html',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: true
                    ])

                    if (params.RUN_ALLURE && fileExists(env.ALLURE_DIR)) {
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: env.ALLURE_DIR]],
                            reportName: 'Allure Report'
                        ])
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('test-results')) {
                    archiveArtifacts artifacts: 'test-results/**', allowEmptyArchive: true
                }
                if (fileExists('allure-results')) {
                    archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
                }
                if (fileExists('salesforce_tab_performance/performance_results.xlsx')) {
                    archiveArtifacts artifacts: 'salesforce_tab_performance/performance_results.xlsx', allowEmptyArchive: true
                }
                if (params.SEND_EMAIL) {
                    sendEmailNotification(currentBuild.currentResult ?: 'UNKNOWN')
                }
            }
        }
    }
}

def buildPytestCommand(String scope, String marker, boolean runAllure) {
    def base = 'pytest -q'
    def selector = ''

    if (scope == 'smoke') {
        selector = '-m smoke'
    } else if (scope == 'marker') {
        selector = "-m ${marker}"
    } else {
        selector = ''
    }

    def allureArg = runAllure ? "--alluredir=${env.ALLURE_DIR}" : ''
    return "${base} ${selector} ${allureArg} --junitxml=${env.PYTEST_JUNIT} --html=${env.PYTEST_HTML} --self-contained-html --json-report --json-report-file=${env.PYTEST_JSON}"
}

def sendEmailNotification(String resultStatus) {
    def defaultEmail = params.DEFAULT_EMAIL?.trim()
    def extraEmails = params.ADDITIONAL_EMAILS?.trim()
    def recipients = []

    if (defaultEmail) {
        recipients.add(defaultEmail)
    }
    if (extraEmails) {
        extraEmails.split(',').collect { it.trim() }.findAll { it }.each { mail ->
            if (!recipients.contains(mail)) {
                recipients.add(mail)
            }
        }
    }
    if (recipients.isEmpty()) {
        echo 'No email recipients configured; skipping email notification.'
        return
    }

    def markerInfo = params.TEST_SCOPE == 'marker' ? params.PYTEST_MARKER : 'N/A'
    def jobUrl = env.BUILD_URL ?: ''
    def excelRelPath = 'salesforce_tab_performance/performance_results.xlsx'
    def excelExists = fileExists(excelRelPath)
    def artifactBase = "${jobUrl}artifact/"
    def excelArtifactUrl = "${artifactBase}${excelRelPath}"
    def subject = "[Dakota Performance] ${resultStatus} - ${env.JOB_NAME} #${env.BUILD_NUMBER}"
    def body = """
    <html>
      <body style="font-family:Segoe UI,Arial,sans-serif;">
        <h2>Dakota Marketplace Performance Pipeline</h2>
        <p><b>Status:</b> ${resultStatus}</p>
        <p><b>Job:</b> ${env.JOB_NAME}</p>
        <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
        <p><b>Scope:</b> ${params.TEST_SCOPE}</p>
        <p><b>Marker:</b> ${markerInfo}</p>
        <p><b>Allure Enabled:</b> ${params.RUN_ALLURE}</p>
        <p><b>Build URL:</b> <a href="${jobUrl}">${jobUrl}</a></p>
        <p><b>Excel Artifact:</b> ${excelExists ? "<a href='${excelArtifactUrl}'>performance_results.xlsx</a>" : "Not generated in this run"}</p>
        <hr/>
        <p>Reports are attached/published in Jenkins artifacts and report tabs.</p>
      </body>
    </html>
    """
    if (excelExists) {
        emailext(
            to: recipients.join(', '),
            subject: subject,
            body: body,
            mimeType: 'text/html',
            attachLog: true,
            compressLog: true,
            attachmentsPattern: excelRelPath
        )
    } else {
        emailext(
            to: recipients.join(', '),
            subject: subject,
            body: body,
            mimeType: 'text/html',
            attachLog: true,
            compressLog: true
        )
    }
}
