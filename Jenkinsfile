pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
        timeout(time: 200, unit: 'MINUTES')
    }

    parameters {
        choice(
            name: 'TEST_SCOPE',
            choices: ['smoke', 'marker', 'full'],
            description: 'Execution mode: smoke (fast sanity), marker (one category), full (complete regression).'
        )
        choice(
            name: 'PYTEST_MARKER',
            choices: ['Test', 'reports', 'metro_areas', 'custom_dashboards', 'accounts', 'contacts', 'documents', 'transactions'],
            description: 'Category to run when TEST_SCOPE=marker. Ignored for smoke/full.'
        )
        booleanParam(
            name: 'RUN_ALLURE',
            defaultValue: true,
            description: 'Publish Allure report in Jenkins (requires Allure plugin installed).'
        )
        booleanParam(
            name: 'ENABLE_INFRA_RETRY',
            defaultValue: true,
            description: 'Retry only infra/transient Selenium failures (not assertion/business-logic failures).'
        )
        string(
            name: 'INFRA_RETRY_COUNT',
            defaultValue: '1',
            description: 'How many retries for allowed infra failures (0 disables retries).'
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
                script {
                    if (fileExists('salesforce_tab_performance/requirements.txt')) {
                        echo 'Repository already present in workspace; skipping checkout.'
                    } else {
                        error(
                            "Workspace has no source code. Configure this job as 'Pipeline script from SCM' " +
                            "or use a Multibranch Pipeline so checkout can pull repository contents."
                        )
                    }
                    def shortCommit = env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : 'N/A'
                    echo "Branch: ${env.BRANCH_NAME ?: 'main'} | Commit: ${shortCommit}"
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    runShell(
                        '''
                            python3 -m venv ${VENV_DIR}
                            ${VENV_DIR}/bin/python -m pip install --upgrade pip
                            ${VENV_DIR}/bin/python -m pip install -r salesforce_tab_performance/requirements.txt
                            ${VENV_DIR}/bin/python -m pip install pytest-html pytest-json-report allure-pytest pytest-rerunfailures
                        ''',
                        '''
                            py -m venv %VENV_DIR%
                            %VENV_DIR%\\Scripts\\python -m pip install --upgrade pip
                            %VENV_DIR%\\Scripts\\python -m pip install -r salesforce_tab_performance/requirements.txt
                            %VENV_DIR%\\Scripts\\python -m pip install pytest-html pytest-json-report allure-pytest pytest-rerunfailures
                        '''
                    )
                }
            }
        }

        stage('Prepare Report Directories') {
            steps {
                script {
                    runShell(
                        '''
                            rm -rf test-results allure-results || true
                            mkdir -p test-results allure-results
                        ''',
                        '''
                            if exist test-results rmdir /s /q test-results
                            if exist allure-results rmdir /s /q allure-results
                            mkdir test-results
                            mkdir allure-results
                        '''
                    )
                }
            }
        }

        stage('Static Validation') {
            steps {
                script {
                    if (params.TEST_SCOPE == 'marker') {
                        if (!params.PYTEST_MARKER?.trim()) {
                            error('PYTEST_MARKER must be provided when TEST_SCOPE=marker.')
                        }
                        echo "Marker mode selected -> running marker: ${params.PYTEST_MARKER}"
                    } else {
                        echo "Scope selected -> ${params.TEST_SCOPE} (marker parameter ignored)"
                    }
                    runPytest('--version')
                    runPytest('--markers')
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def runCmd = buildPytestCommand(
                        params.TEST_SCOPE as String,
                        params.PYTEST_MARKER as String,
                        params.RUN_ALLURE as boolean,
                        params.ENABLE_INFRA_RETRY as boolean,
                        params.INFRA_RETRY_COUNT as String
                    )
                    echo "Pytest command: pytest ${runCmd}"

                    withCredentials([usernamePassword(
                        credentialsId: "${params.SF_CREDENTIALS_ID}",
                        usernameVariable: 'SF_USERNAME',
                        passwordVariable: 'SF_PASSWORD'
                    )]) {
                        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                            runPytest(runCmd)
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

                    try {
                        publishHTML(target: [
                            reportName: 'Pytest HTML Report',
                            reportDir: 'test-results',
                            reportFiles: 'report.html',
                            keepAll: true,
                            alwaysLinkToLastBuild: true,
                            allowMissing: true
                        ])
                    } catch (MissingMethodException ex) {
                        echo 'HTML Publisher plugin not installed; skipping publishHTML step.'
                    }

                    if (params.RUN_ALLURE && fileExists(env.ALLURE_DIR)) {
                        allure([
                            commandline: 'allure-2.34.1',
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: env.ALLURE_DIR]],
                            reportName: 'Allure Report'
                        ])
                    } else if (params.RUN_ALLURE) {
                        echo "Skipping Allure publish: ${env.ALLURE_DIR} directory not found."
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

def buildPytestCommand(String scope, String marker, boolean runAllure, boolean enableInfraRetry, String infraRetryCount) {
    def selector = ''

    if (scope == 'smoke') {
        selector = '-m smoke'
    } else if (scope == 'marker') {
        selector = "-m ${marker}"
    } else {
        selector = ''
    }

    def allureArg = runAllure ? "--alluredir=${env.ALLURE_DIR}" : ''
    def parts = []

    // Show richer live output in Jenkins console:
    // -vv  : print each test node id as it runs
    // -ra  : include skip/xfail/etc summary in terminal output
    // --tb=short : concise failure tracebacks for readability
    // --color=no : avoid ANSI artifacts in Jenkins logs
    // -o console_output_style=progress : keep visible progress counters
    parts << '-vv'
    parts << '-ra'
    parts << '--tb=short'
    parts << '--color=no'
    parts << '-o'
    parts << 'console_output_style=progress'

    if (selector) {
        parts << selector
    }
    if (allureArg) {
        parts << allureArg
    }

    if (enableInfraRetry) {
        def retries = 0
        try {
            retries = Math.max((infraRetryCount ?: '0').trim() as int, 0)
        } catch (Exception ignored) {
            retries = 1
        }

        if (retries > 0) {
            // Requires pytest-rerunfailures plugin. Keep this list focused on transient/UI infra issues.
            parts << "--reruns=${retries}"
            parts << '--only-rerun=selenium\\.common\\.exceptions\\.TimeoutException'
            parts << '--only-rerun=selenium\\.common\\.exceptions\\.NoSuchElementException'
            parts << '--only-rerun=selenium\\.common\\.exceptions\\.StaleElementReferenceException'
            parts << '--only-rerun=selenium\\.common\\.exceptions\\.ElementClickInterceptedException'
            parts << '--only-rerun=selenium\\.common\\.exceptions\\.WebDriverException'
        }
    }

    parts << "--junitxml=${env.PYTEST_JUNIT}"
    parts << "--html=${env.PYTEST_HTML}"
    parts << '--self-contained-html'
    parts << '--json-report'
    parts << "--json-report-file=${env.PYTEST_JSON}"

    return parts.join(' ')
}

def runShell(String unixCommand, String windowsCommand) {
    if (isUnix()) {
        sh(unixCommand)
    } else {
        bat(windowsCommand)
    }
}

def runPytest(String args) {
    runShell(
        """
            ${env.VENV_DIR}/bin/python -m pytest ${args}
        """,
        """
            %VENV_DIR%\\Scripts\\python -m pytest ${args}
        """
    )
}

def getTestStatistics() {
    def stats = [total: 0, passed: 0, failed: 0, skipped: 0]
    def reportPath = env.PYTEST_JSON ?: 'test-results/report.json'
    def junitPath = env.PYTEST_JUNIT ?: 'test-results/pytest.xml'

    if (fileExists(reportPath)) {
        try {
            def jsonText = readFile(reportPath)
            stats.passed = extractIntFromJson(jsonText, 'passed')
            stats.failed = extractIntFromJson(jsonText, 'failed')
            stats.skipped = extractIntFromJson(jsonText, 'skipped')
            stats.total = stats.passed + stats.failed + stats.skipped
        } catch (Exception ex) {
            echo "Could not parse pytest JSON report: ${ex.message}"
        }
    } else {
        echo "Pytest JSON report not found at ${reportPath}; trying JUnit fallback."
    }

    if (stats.total == 0 && fileExists(junitPath)) {
        try {
            def xmlText = readFile(junitPath)
            def tests = extractIntFromXmlAttribute(xmlText, 'tests')
            def failures = extractIntFromXmlAttribute(xmlText, 'failures')
            def errors = extractIntFromXmlAttribute(xmlText, 'errors')
            def skipped = extractIntFromXmlAttribute(xmlText, 'skipped')
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

def extractIntFromJson(String jsonText, String key) {
    if (!jsonText?.trim()) {
        return 0
    }
    def matcher = (jsonText =~ /"${java.util.regex.Pattern.quote(key)}"\s*:\s*(\d+)/)
    if (matcher.find()) {
        return (matcher.group(1) ?: '0') as int
    }
    return 0
}

def extractIntFromXmlAttribute(String xmlText, String attr) {
    if (!xmlText?.trim()) {
        return 0
    }
    def matcher = (xmlText =~ /${java.util.regex.Pattern.quote(attr)}\s*=\s*["'](\d+)["']/)
    if (matcher.find()) {
        return (matcher.group(1) ?: '0') as int
    }
    return 0
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
    def actualStatus = currentBuild.result ?: buildStatus

    // Preserve Jenkins infra/build failures as source of truth.
    if (!(actualStatus in ['FAILURE', 'ABORTED'])) {
        if (stats.total == 0) {
            actualStatus = 'UNSTABLE'
        } else if (stats.failed > 0) {
            actualStatus = 'FAILURE'
        } else {
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
    echo "Excel exists: ${excelExists}"
    def excelArtifactUrl = "${artifactBase}${excelRelPath}"
    def htmlReportUrl = "${artifactBase}test-results/report.html"
    def allureUrl = "${jobUrl}allure"
    def passRate = stats.total > 0 ? ((stats.passed * 100) / stats.total) as int : 0
    def triggeredBy = env.BUILD_USER ?: env.BUILD_USER_ID ?: 'Jenkins'
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
                <tr><td width="32%"><strong>Build</strong></td><td><a style="color:#2563eb;text-decoration:underline;" href="${jobUrl}">${jobUrl}</a></td></tr>
                <tr><td><strong>HTML Report</strong></td><td><a style="color:#2563eb;text-decoration:underline;" href="${htmlReportUrl}">test-results/report.html</a></td></tr>
                <tr><td><strong>Allure Report</strong></td><td><a style="color:#2563eb;text-decoration:underline;" href="${allureUrl}">${allureUrl}</a></td></tr>
                <tr><td><strong>Excel Artifact</strong></td><td>${excelExists ? "<a style='color:#2563eb;text-decoration:underline;' href='${excelArtifactUrl}'>performance_results.xlsx</a>" : "Not generated in this run"}</td></tr>
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
