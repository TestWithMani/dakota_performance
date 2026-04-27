# Jenkins CI/CD Setup (Local)

This project includes a production-style `Jenkinsfile` at the repository root.

## 1) Jenkins Prerequisites

On your Jenkins server/agent:

- Python installed (`py` on Windows or `python3` on Linux)
- Google Chrome installed (for Selenium UI tests)
- Internet/network access to Salesforce target environment

Recommended Jenkins plugins:

- Pipeline
- Credentials Binding
- JUnit
- Git
- HTML Publisher
- Email Extension
- Allure Jenkins Plugin (optional, if `RUN_ALLURE=true`)
- Workspace Cleanup (optional)

## 2) Create Credentials in Jenkins

In Jenkins (`http://localhost:8080`):

1. Go to `Manage Jenkins` -> `Credentials` -> `(global)` -> `Add Credentials`.
2. Kind: `Username with password`.
3. ID: `sf-marketplace-creds` (or any ID, then update pipeline parameter).
4. Username: Salesforce username.
5. Password: Salesforce password.

## 3) Create Pipeline Job

1. `New Item` -> `Pipeline` -> name it `dakota-performance`.
2. Under `Pipeline` section:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: your GitHub repo URL
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`

Save, then run `Build with Parameters`.

## 4) Pipeline Parameters

This pipeline uses checkbox-driven test selection:

- `TEST_SELECTION_MODE`
  - `ALL_TABS` -> run all mapped test files
  - `CHECKBOX_SELECTION` -> run only checked `TAB_*` parameters
- `TAB_*` checkboxes
  - Each checkbox maps to one test file in `tests/` (for example `TAB_MARKETPLACE_HOME`).
- `RUN_ALLURE`
  - Publish Allure report from `allure-results`.
- `ENABLE_INFRA_RETRY`
  - Enables flaky infra retry for Selenium-style failures.
- `INFRA_RETRY_COUNT`
  - Number of allowed infra retries (string integer, default `1`).
- `FRESH_REPORT_OUTPUT`
  - Clears previous report artifacts and produces fresh outputs.
- `SEND_EMAIL`
  - Sends HTML summary email after run.
- `DEFAULT_EMAIL`, `ADDITIONAL_EMAILS`
  - Recipient controls for email notifications.
- `SF_CREDENTIALS_ID`
  - Jenkins credentials ID for Salesforce username/password.
- `ALLURE_TOOL_NAME`
  - Optional Jenkins Allure commandline tool name.
- `RESET_JOB_BUILD_HISTORY`
  - Safe cleanup mode in current implementation (workspace artifacts only).

## 5) Suggested Job Strategy

- **PR validation job**:
  - `TEST_SELECTION_MODE=CHECKBOX_SELECTION` and only a small smoke subset of `TAB_*` checkboxes.
- **Scheduled full regression**:
  - `TEST_SELECTION_MODE=ALL_TABS`
  - `ENABLE_INFRA_RETRY=true`, `INFRA_RETRY_COUNT=1`
- **Focused category jobs**:
  - Keep `TEST_SELECTION_MODE=CHECKBOX_SELECTION`
  - Select only the relevant `TAB_*` group per job.

## 6) Artifacts and Reports

Pipeline archives:

- `test-results/**` (includes JUnit XML, HTML report, JSON report)
- `allure-results/**` (if enabled)
- Excel artifact from:
  - `salesforce_tab_performance/Dakota Marketplace Performance.xlsx` (preferred)
  - fallback sources are auto-resolved by pipeline

## 7) Notes

- UI tests require a stable browser session on the Jenkins agent.
- If your Jenkins agent runs as a Windows service and UI tests are unstable, run Jenkins agent interactively or use a dedicated test node.
- For freestyle pipeline jobs, this repository must exist in workspace before execution. Recommended setup is **Pipeline script from SCM** (or Multibranch Pipeline).
