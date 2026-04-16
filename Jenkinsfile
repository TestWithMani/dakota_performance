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

                    logTestSummaryToConsole('Post test execution')
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
                logTestSummaryToConsole('Post pipeline summary')
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

def getTestStatistics() {
    def stats = [total: 0, passed: 0, failed: 0, skipped: 0]
    def reportPath = env.PYTEST_JSON ?: 'test-results/report.json'
    def junitPath = env.PYTEST_JUNIT ?: 'test-results/pytest.xml'

    if (fileExists(reportPath)) {
        try {
            def report = new groovy.json.JsonSlurper().parseText(readFile(reportPath))
            stats.passed = (report?.summary?.passed ?: 0) as int
            stats.failed = (report?.summary?.failed ?: 0) as int
            stats.skipped = (report?.summary?.skipped ?: 0) as int
            stats.total = stats.passed + stats.failed + stats.skipped
        } catch (Exception ex) {
            echo "Could not parse pytest JSON report: ${ex.message}"
        }
    } else {
        echo "Pytest JSON report not found at ${reportPath}; trying JUnit fallback."
    }

    if (stats.total == 0 && fileExists(junitPath)) {
        try {
            def xml = new XmlSlurper(false, false).parseText(readFile(junitPath))
            def tests = (xml.@tests?.toString() ?: '0') as int
            def failures = (xml.@failures?.toString() ?: '0') as int
            def errors = (xml.@errors?.toString() ?: '0') as int
            def skipped = (xml.@skipped?.toString() ?: '0') as int
            def passed = Math.max(tests - failures - errors - skipped, 0)

            stats.total = tests
            stats.failed = failures + errors
            stats.skipped = skipped
            stats.passed = passed
            echo "Using JUnit fallback stats -> total:${stats.total}, passed:${stats.passed}, failed:${stats.failed}, skipped:${stats.skipped}"
        } catch (Exception ex) {
            echo "Could not parse JUnit XML fallback: ${ex.message}"
        }
    }

    return stats
}

def logTestSummaryToConsole(String label = 'Test summary') {
    def stats = getTestStatistics()
    echo """
================ ${label} ================
Total  : ${stats.total}
Passed : ${stats.passed}
Failed : ${stats.failed}
Skipped: ${stats.skipped}
==========================================
""".stripIndent()
}

def sendEmailNotification(String buildStatus) {
    def stats = getTestStatistics()
    def actualStatus = buildStatus

    if (stats.total > 0) {
        if (stats.failed > 0) {
            actualStatus = 'FAILURE'
        } else if (stats.passed > 0) {
            actualStatus = 'SUCCESS'
        }
    }

    def recipients = []
    if (params.DEFAULT_EMAIL?.trim()) {
        recipients.add(params.DEFAULT_EMAIL.trim())
    }
    if (params.ADDITIONAL_EMAILS?.trim()) {
        params.ADDITIONAL_EMAILS.split(',').collect { it.trim() }.findAll { it }.each { mail ->
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
    def artifactBase = "${jobUrl}artifact/"
    def excelRelPath = 'salesforce_tab_performance/performance_results.xlsx'
    def excelExists = fileExists(excelRelPath)
    def excelArtifactUrl = "${artifactBase}${excelRelPath}"
    def htmlReportUrl = "${artifactBase}test-results/report.html"
    def allureUrl = "${jobUrl}allure"
    def passRate = stats.total > 0 ? ((stats.passed * 100) / stats.total) as int : 0
    def triggeredBy = env.BUILD_USER_ID ?: 'Jenkins'
    def durationString = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')

    def statusCfg = [
        SUCCESS : [bg: '#ecfdf5', border: '#10b981', text: '#065f46'],
        FAILURE : [bg: '#fef2f2', border: '#ef4444', text: '#991b1b'],
        UNSTABLE: [bg: '#fffbeb', border: '#f59e0b', text: '#92400e']
    ]
    def cfg = statusCfg.get(actualStatus, statusCfg.UNSTABLE)
    def subject = "Dakota Performance Report | ${actualStatus} | #${env.BUILD_NUMBER}"

    def body = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Dakota Performance Report</title>
</head>
<body style="margin:0;padding:0;background:#f1f5f9;font-family:Segoe UI,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td align="center" style="padding:24px;">
        <table width="760" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #e2e8f0;">
          <tr>
            <td style="padding:24px 28px;background:linear-gradient(135deg,#1d4ed8 0%,#2563eb 100%);color:#ffffff;">
              <h2 style="margin:0;font-size:24px;">Dakota Marketplace Performance</h2>
              <p style="margin:6px 0 0;font-size:14px;opacity:0.95;">Automated Jenkins Test Execution Report</p>
            </td>
          </tr>

          <tr>
            <td style="padding:14px 28px;background:${cfg.bg};border-bottom:1px solid ${cfg.border};color:${cfg.text};">
              <table width="100%">
                <tr>
                  <td style="font-size:18px;font-weight:700;">Status: ${actualStatus}</td>
                  <td align="right" style="font-size:14px;">Pass Rate: <strong>${passRate}%</strong></td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:20px 24px;background:#f8fafc;">
              <table width="100%" cellpadding="8" cellspacing="8">
                <tr align="center">
                  <td style="background:#2563eb;color:#fff;border-radius:10px;"><div style="font-size:12px;">TOTAL</div><div style="font-size:28px;font-weight:700;">${stats.total}</div></td>
                  <td style="background:#16a34a;color:#fff;border-radius:10px;"><div style="font-size:12px;">PASSED</div><div style="font-size:28px;font-weight:700;">${stats.passed}</div></td>
                  <td style="background:#dc2626;color:#fff;border-radius:10px;"><div style="font-size:12px;">FAILED</div><div style="font-size:28px;font-weight:700;">${stats.failed}</div></td>
                  <td style="background:#7c3aed;color:#fff;border-radius:10px;"><div style="font-size:12px;">SKIPPED</div><div style="font-size:28px;font-weight:700;">${stats.skipped}</div></td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:22px 28px;">
              <h3 style="margin:0 0 10px;color:#0f172a;">Build Details</h3>
              <table width="100%" cellpadding="8" cellspacing="0" style="font-size:14px;color:#1e293b;">
                <tr><td width="32%"><strong>Job</strong></td><td>${env.JOB_NAME}</td></tr>
                <tr><td><strong>Build #</strong></td><td>${env.BUILD_NUMBER}</td></tr>
                <tr><td><strong>Scope</strong></td><td>${params.TEST_SCOPE}</td></tr>
                <tr><td><strong>Marker</strong></td><td>${markerInfo}</td></tr>
                <tr><td><strong>Duration</strong></td><td>${durationString}</td></tr>
                <tr><td><strong>Triggered By</strong></td><td>${triggeredBy}</td></tr>
              </table>

              <h3 style="margin:16px 0 10px;color:#0f172a;">Reports</h3>
              <table width="100%" cellpadding="8" cellspacing="0" style="font-size:14px;">
                <tr><td width="32%"><strong>Build</strong></td><td><a href="${jobUrl}">${jobUrl}</a></td></tr>
                <tr><td><strong>HTML Report</strong></td><td><a href="${htmlReportUrl}">test-results/report.html</a></td></tr>
                <tr><td><strong>Allure Report</strong></td><td><a href="${allureUrl}">${allureUrl}</a></td></tr>
                <tr><td><strong>Excel Artifact</strong></td><td>${excelExists ? "<a href='${excelArtifactUrl}'>performance_results.xlsx</a>" : "Not generated in this run"}</td></tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:14px 28px;background:#0f172a;color:#cbd5e1;font-size:12px;">
              Automated by Jenkins CI/CD | Dakota Marketplace Test Framework
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    def commonArgs = [
        to: recipients.join(', '),
        subject: subject,
        body: body,
        mimeType: 'text/html',
        attachLog: true,
        compressLog: true
    ]

    if (excelExists) {
        emailext(commonArgs + [attachmentsPattern: excelRelPath])
    } else {
        emailext(commonArgs)
    }
}
