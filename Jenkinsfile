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
        booleanParam(
            name: 'FRESH_REPORT_OUTPUT',
            defaultValue: false,
            description: 'When enabled, clear prior Allure/Excel history and generate a fresh dated Excel attachment.'
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
                    if (params.FRESH_REPORT_OUTPUT as boolean) {
                        echo 'Fresh report mode enabled: clearing previous Excel and Allure history artifacts.'
                        runShell(
                            '''
                                rm -f salesforce_tab_performance/performance_results.xlsx || true
                                rm -f "salesforce_tab_performance/Dakota Marketplace Performance.xlsx" || true
                                rm -f salesforce_tab_performance/*.xlsx || true
                                rm -rf allure-report || true
                            ''',
                            '''
                                if exist "salesforce_tab_performance\\performance_results.xlsx" del /q "salesforce_tab_performance\\performance_results.xlsx"
                                if exist "salesforce_tab_performance\\Dakota Marketplace Performance.xlsx" del /q "salesforce_tab_performance\\Dakota Marketplace Performance.xlsx"
                                del /q "salesforce_tab_performance\\Dakota Matketplace Performance - *.xlsx" 2>nul
                                if exist allure-report rmdir /s /q allure-report
                            '''
                        )
                    }
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
                def excelArtifact = prepareExcelArtifactPath(params.FRESH_REPORT_OUTPUT as boolean)
                if (excelArtifact) {
                    archiveArtifacts artifacts: excelArtifact, allowEmptyArchive: true
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

    def recipients = collectRecipientEmails(
        params.DEFAULT_EMAIL as String,
        params.ADDITIONAL_EMAILS as String
    )
    if (recipients.isEmpty()) {
        echo 'No email recipients configured; skipping email notification.'
        return
    }

    def jobUrl = env.BUILD_URL ?: ''
    def excelRelPath = prepareExcelArtifactPath(params.FRESH_REPORT_OUTPUT as boolean)
    def excelExists = excelRelPath ? fileExists(excelRelPath) : false
    def allureUrl = "${jobUrl}allure"
    def durationString = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')
    def passRate = stats.total > 0 ? ((stats.passed * 100) / stats.total) as int : 0

    def statusCfg = [
        SUCCESS : [bg: '#ecfdf5', border: '#10b981', text: '#065f46', pillBg: '#dcfce7'],
        FAILURE : [bg: '#fef2f2', border: '#ef4444', text: '#991b1b', pillBg: '#fee2e2'],
        ABORTED : [bg: '#f8fafc', border: '#64748b', text: '#334155', pillBg: '#e2e8f0'],
        UNSTABLE: [bg: '#fffbeb', border: '#f59e0b', text: '#92400e', pillBg: '#fef3c7']
    ]
    def cfg = statusCfg.get(actualStatus, statusCfg.UNSTABLE)
    def subject = "Dakota Marketplace Performnace | ${new Date().format('yyyy-MM-dd')}"

    def body = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Dakota Performance Report</title>
</head>
<body style="margin:0;padding:0;background:linear-gradient(140deg,#e0ecff 0%,#efe7ff 45%,#fff6e5 100%);font-family:'Segoe UI',Roboto,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td align="center" style="padding:24px;">
        <table width="760" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #dbe3ee;box-shadow:0 14px 32px rgba(30,64,175,0.14);">
          <tr>
            <td style="padding:26px 30px;background:linear-gradient(135deg,#0f172a 0%,#1e40af 52%,#7c3aed 100%);color:#ffffff;">
              <h2 style="margin:0;font-size:24px;letter-spacing:0.2px;">Dakota Marketplace Performance</h2>
              <p style="margin:8px 0 0;font-size:13px;opacity:0.92;">Automated CI execution summary for your latest run</p>
            </td>
          </tr>

          <tr>
            <td style="padding:16px 28px;background:${cfg.bg};border-bottom:1px solid ${cfg.border};color:${cfg.text};">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="font-size:18px;font-weight:700;">Execution Status</td>
                  <td align="right">
                    <span style="display:inline-block;padding:7px 12px;border-radius:999px;font-size:12px;font-weight:700;background:${cfg.pillBg};color:${cfg.text};border:1px solid ${cfg.border};">
                      ${actualStatus}
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:24px 30px 10px;">
              <h3 style="margin:0 0 12px;color:#0f172a;font-size:17px;">Build Details</h3>
              <table width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;color:#1e293b;border:1px solid #c7d2fe;border-radius:10px;overflow:hidden;background:linear-gradient(180deg,#f8faff 0%,#fdfdff 100%);">
                <tr><td width="32%" style="padding:10px 12px;background:linear-gradient(180deg,#e0e7ff 0%,#eef2ff 100%);border-bottom:1px solid #c7d2fe;"><strong>Build Number</strong></td><td style="padding:10px 12px;border-bottom:1px solid #dbe3f3;">#${env.BUILD_NUMBER}</td></tr>
                <tr><td style="padding:10px 12px;background:linear-gradient(180deg,#e0e7ff 0%,#eef2ff 100%);border-bottom:1px solid #c7d2fe;"><strong>Scope</strong></td><td style="padding:10px 12px;border-bottom:1px solid #dbe3f3;">${params.TEST_SCOPE}</td></tr>
                <tr><td style="padding:10px 12px;background:linear-gradient(180deg,#e0e7ff 0%,#eef2ff 100%);border-top:1px solid #c7d2fe;"><strong>Duration</strong></td><td style="padding:10px 12px;border-top:1px solid #dbe3f3;">${durationString}</td></tr>
                <tr><td style="padding:10px 12px;background:linear-gradient(180deg,#e0e7ff 0%,#eef2ff 100%);border-top:1px solid #c7d2fe;"><strong>Passed Percentage</strong></td><td style="padding:10px 12px;border-top:1px solid #dbe3f3;color:#0f766e;font-weight:700;">${passRate}%</td></tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:8px 30px 24px;">
              <h3 style="margin:0 0 12px;color:#0f172a;font-size:17px;">Report Access</h3>
              <table width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;color:#1e293b;border:1px solid #c4b5fd;border-radius:10px;overflow:hidden;background:linear-gradient(180deg,#faf5ff 0%,#f3f0ff 100%);">
                <tr>
                  <td width="32%" style="padding:10px 12px;background:linear-gradient(180deg,#ede9fe 0%,#ddd6fe 100%);"><strong>Allure Report</strong></td>
                  <td style="padding:10px 12px;">
                    <a style="color:#6d28d9;text-decoration:underline;font-weight:700;" href="${allureUrl}">Open Allure Report</a>
                  </td>
                </tr>
              </table>
              <p style="margin:12px 0 0;color:#64748b;font-size:12px;">Please see the attached Excel performance sheet for detailed run metrics.</p>
            </td>
          </tr>

          <tr>
            <td style="padding:0 30px 20px;">
              <table width="100%" cellpadding="8" cellspacing="8" style="font-size:13px;">
                <tr align="center">
                  <td style="background:linear-gradient(180deg,#dbeafe 0%,#bfdbfe 100%);color:#1e3a8a;border-radius:9px;"><div style="font-size:11px;">TOTAL</div><div style="font-size:22px;font-weight:700;">${stats.total}</div></td>
                  <td style="background:linear-gradient(180deg,#dcfce7 0%,#bbf7d0 100%);color:#065f46;border-radius:9px;"><div style="font-size:11px;">PASSED</div><div style="font-size:22px;font-weight:700;">${stats.passed}</div></td>
                  <td style="background:linear-gradient(180deg,#fee2e2 0%,#fecaca 100%);color:#991b1b;border-radius:9px;"><div style="font-size:11px;">FAILED</div><div style="font-size:22px;font-weight:700;">${stats.failed}</div></td>
                  <td style="background:linear-gradient(180deg,#ede9fe 0%,#ddd6fe 100%);color:#5b21b6;border-radius:9px;"><div style="font-size:11px;">SKIPPED</div><div style="font-size:22px;font-weight:700;">${stats.skipped}</div></td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:13px 30px;background:#0f172a;color:#cbd5e1;font-size:12px;">
              Jenkins CI/CD • Dakota Marketplace Test Framework
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    def baseArgs = [
        subject: subject,
        body: body,
        mimeType: 'text/html',
        attachLog: false,
        compressLog: false
    ]
    if (excelExists) {
        baseArgs.attachmentsPattern = excelRelPath
    }

    def recipientList = recipients.join(', ')
    echo "Sending email to: ${recipientList}"

    try {
        // Primary path: single send with comma-separated recipients (same as prior working pipeline).
        emailext(baseArgs + [to: recipientList])
    } catch (Exception ex) {
        echo "Combined email send failed: ${ex.getMessage()}"
        echo "Falling back to one-by-one recipient delivery."
        recipients.each { recipient ->
            try {
                echo "Sending fallback email to: ${recipient}"
                emailext(baseArgs + [to: recipient])
            } catch (Exception innerEx) {
                echo "Failed to send email to ${recipient}: ${innerEx.getMessage()}"
            }
        }
    }
}

def prepareExcelArtifactPath(boolean freshMode) {
    def baseDir = 'salesforce_tab_performance'
    def defaultExcel = "${baseDir}/performance_results.xlsx"
    def finalExcel = "${baseDir}/Dakota Marketplace Performance.xlsx"
    if (!fileExists(defaultExcel)) {
        return null
    }

    if (defaultExcel != finalExcel) {
        runShell(
            """
                cp "${defaultExcel}" "${finalExcel}"
            """,
            """
                copy /Y "${defaultExcel}" "${finalExcel}" >nul
            """
        )
    }
    return finalExcel
}

def collectRecipientEmails(String defaultEmail, String additionalEmails) {
    def recipients = []
    def seen = [] as Set

    // Pass through any domain and keep parsing tolerant for separators/whitespace.
    [defaultEmail, additionalEmails].findAll { it?.trim() }.each { source ->
        source
            .split(/[,\s;]+/)
            .collect { it.trim() }
            .findAll { it }
            .each { mail ->
                def normalized = mail.toLowerCase()
                if (!seen.contains(normalized)) {
                    seen.add(normalized)
                    recipients.add(mail)
                }
            }
    }

    echo "Email recipients resolved: ${recipients.join(', ')}"
    return recipients
}
