# Dakota Marketplace Performance Suite

Python + Selenium + pytest framework for measuring Salesforce tab render performance in Dakota Marketplace.

## What This Project Does

This suite opens Dakota Marketplace tabs in a real browser, measures load/render completion time using configurable page readiness signals, runs multiple timing iterations, and writes a final benchmark outcome (PASS/FAIL) against an SLA threshold.

It is designed for:
- local developer validation,
- smoke/full/regression execution by markers,
- Jenkins parameterized runs (single tab, smoke set, or full suite),
- CI sanity checks for test/marker discovery.

## Key Capabilities

- Configurable start/end locator timing model for each tab flow.
- Completion strategy per tab (`visible` or `clickable` end condition).
- Iteration-based timing with averaged final result.
- Excel export for historical performance records.
- Allure attachments for failed test diagnostics (URL, page source, screenshot).
- Browser selection from CLI (`chrome`, `edge`, `firefox`).
- Marker-driven execution (`smoke`, `full`, and category markers).

## Project Structure

```text
MP_Performance/
├── salesforce_tab_performance/
│   ├── config.py                 # runtime configuration (iterations, SLA, locators, waits)
│   ├── credentials_utils.py      # credential bootstrapping from env/.env/Windows storage
│   ├── performance_utils.py      # timing and tab performance helpers
│   ├── tab_test_runner.py        # common execution flow used by tests
│   ├── excel_logger.py           # writes timing results to Excel
│   └── requirements.txt          # Python dependencies
├── tests/
│   ├── conftest.py               # WebDriver fixture, browser option, marker auto-tagging
│   └── test_*_tab_performance.py # per-tab performance tests
├── docs/
│   └── JENKINS_SETUP.md          # local Jenkins setup and job guidance
├── .github/workflows/ci.yml      # GitHub Actions discovery validation
├── Jenkinsfile                   # parameterized CI/CD pipeline
├── pytest.ini                    # declared markers
└── README.md
```

## Requirements

- Python 3.10+ (CI currently validates on Python 3.11)
- One supported browser installed:
  - Google Chrome, or
  - Microsoft Edge, or
  - Mozilla Firefox
- Network access to the Dakota Salesforce environment
- Valid Salesforce credentials (`SF_USERNAME`, `SF_PASSWORD`)

## Quick Start (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r salesforce_tab_performance/requirements.txt
```

Set credentials for the current shell:

```powershell
$env:SF_USERNAME="your_username"
$env:SF_PASSWORD="your_password"
```

Set credentials persistently on Windows:

```powershell
setx SF_USERNAME "your_username"
setx SF_PASSWORD "your_password"
```

Open a new terminal after `setx` so values are loaded.

## Credentials and Environment

This project uses `salesforce_tab_performance/credentials_utils.py` to bootstrap credentials before tests execute.

Supported sources (in practical priority order):
- process environment variables (`SF_USERNAME`, `SF_PASSWORD`),
- persisted Windows environment values,
- `.env` file fallback.

If using `.env`, create it in the repository root with:

```env
SF_USERNAME=your_username
SF_PASSWORD=your_password
```

Do not commit real credentials.

## Running Tests

Run full suite:

```powershell
pytest -q
```

Run smoke suite:

```powershell
pytest -q -m smoke
```

Run category suites:

```powershell
pytest -q -m Test
pytest -q -m accounts
pytest -q -m contacts
pytest -q -m documents
pytest -q -m transactions
pytest -q -m metro_areas
pytest -q -m reports
pytest -q -m custom_dashboards
```

Select browser:

```powershell
pytest -q --browser chrome
pytest -q --browser edge
pytest -q --browser firefox
```

Generate Allure results:

```powershell
pytest -q --alluredir=allure-results
```

Discovery/validation checks:

```powershell
pytest -q --collect-only
pytest -q -m smoke --collect-only
```

## Marker Reference

Markers are declared in `pytest.ini` and assigned dynamically in `tests/conftest.py`.

- `smoke`: high-signal smoke subset
- `full`: applied to all tests
- `Test`: marketplace home tab family
- `accounts`, `contacts`, `documents`, `transactions`
- `metro_areas`, `reports`, `custom_dashboards`

## Runtime Configuration

Main runtime settings are in `salesforce_tab_performance/config.py`, including:
- timing iteration count,
- SLA threshold in seconds,
- stabilization wait strategy,
- tab-specific locator definitions and completion mode.

Adjust these values to tune sensitivity, benchmark policy, and tab completion conditions.

## Output and Reports

Typical outputs:
- Excel performance workbook in `salesforce_tab_performance/` (pipeline expects `Dakota Marketplace Performance.xlsx`)
- Test result artifacts under `test-results/` (JUnit XML, HTML, JSON in CI contexts)
- Allure raw results in `allure-results/` when enabled

On test failure, Allure attachments include:
- current URL,
- page source,
- screenshot image.

## CI/CD

### GitHub Actions

Workflow: `.github/workflows/ci.yml`

Runs on push/PR to `main` and performs:
- dependency installation,
- test discovery validation (`pytest --collect-only`),
- marker subset discovery checks.

This workflow validates structure and marker health, not full browser performance execution.

### Jenkins Pipeline

Pipeline: `Jenkinsfile`  
Setup guide: `docs/JENKINS_SETUP.md`

Core Jenkins capabilities:
- execution modes: `ALL_TABS`, `SMOKE`, `CHECKBOX_SELECTION`,
- tab-level checkboxes (`TAB_*`) for focused runs,
- optional infra retry handling,
- optional Allure publishing,
- JUnit/HTML/JSON result publication,
- Excel artifact archiving,
- optional email summary notifications.

## Infrastructure Failures (WebDriver Timeouts)

Jenkins can automatically **retry** and then **skip** browser/driver infrastructure failures (for example `ReadTimeoutError` talking to `localhost` chromedriver) when:

- `ENABLE_INFRA_RETRY=true`
- `INFRA_RETRY_COUNT` is at least `1`

Skipped infrastructure tests appear in Allure/JUnit as **skipped** (reason prefix `INFRA_SKIP:`), not failed. Tab SLA/assertion failures still fail the run.

## Troubleshooting

- Credentials not found:
  - verify `SF_USERNAME` and `SF_PASSWORD` in current shell (`echo $env:SF_USERNAME` in PowerShell).
- Browser startup errors:
  - ensure selected browser is installed and updated.
- Unstable UI execution on Jenkins Windows service agents:
  - run the agent in an interactive session or use a dedicated UI node.
- Empty/partial test selection:
  - run `pytest -q --collect-only` and confirm marker names match `pytest.ini`.

## Contributing

See `CONTRIBUTING.md` for branch, testing, and PR guidance.

## License

This project is licensed under the MIT License. See `LICENSE`.
