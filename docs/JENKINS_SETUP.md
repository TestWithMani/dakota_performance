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

- `TEST_SCOPE`
  - `smoke`
  - `marker`
  - `full`
- `PYTEST_MARKER` (used only with `marker`)
- `RUN_ALLURE` (generate `allure-results`)
- `SF_CREDENTIALS_ID` (default: `sf-marketplace-creds`)

## 5) Suggested Job Strategy

- **PR validation job**: use GitHub Actions `pytest -q --collect-only`
- **Scheduled regression job**: `TEST_SCOPE=smoke`
- **Category jobs**:
  - `TEST_SCOPE=marker`, `PYTEST_MARKER=Test` (Marketplace Home tab test)
  - `TEST_SCOPE=marker`, `PYTEST_MARKER=reports`
  - `TEST_SCOPE=marker`, `PYTEST_MARKER=metro_areas`
  - `TEST_SCOPE=marker`, `PYTEST_MARKER=custom_dashboards`

## 6) Artifacts and Reports

Pipeline archives:

- `allure-results/**` (if enabled)
- `salesforce_tab_performance/performance_results.xlsx`
- `test-results/pytest.xml` (JUnit report)

## 7) Notes

- UI tests require a stable browser session on the Jenkins agent.
- If your Jenkins agent runs as a Windows service and UI tests are unstable, run Jenkins agent interactively or use a dedicated test node.
