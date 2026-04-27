# Dakota Marketplace Performance Suite

Python + Selenium + pytest framework for measuring Salesforce tab render performance in Dakota Marketplace.

## Highlights

- Measures UI render completion time with configurable start/end locators.
- Supports per-tab completion rules (`visible` or `clickable`).
- Runs multiple iterations, calculates average, and evaluates SLA in one final summary result.
- Exports run data to Excel and captures failure artifacts in Allure.
- Includes marker-based test grouping for smoke/full/category execution.

## Project Layout

```text
MP_Performance/
├── salesforce_tab_performance/
│   ├── config.py
│   ├── credentials_utils.py
│   ├── excel_logger.py
│   ├── performance_utils.py
│   └── tab_test_runner.py
├── tests/
├── pytest.ini
└── README.md
```

## Prerequisites

- Python 3.10+
- Google Chrome installed
- Salesforce credentials for Dakota Marketplace

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r salesforce_tab_performance/requirements.txt
```

Set credentials (PowerShell):

```powershell
$env:SF_USERNAME="your_username"
$env:SF_PASSWORD="your_password"
```

Persistent (Windows):

```powershell
setx SF_USERNAME "your_username"
setx SF_PASSWORD "your_password"
```

## Run Tests

Run all:

```bash
pytest -q
```

Run smoke:

```bash
pytest -q -m smoke
```

Run category examples:

```bash
pytest -q -m Test
pytest -q -m metro_areas
pytest -q -m reports
pytest -q -m custom_dashboards
```

Run with Allure output:

```bash
pytest --alluredir=allure-results
```

## Reporting

- Excel output file: `salesforce_tab_performance/performance_results.xlsx`
- Iteration rows contain sample timings.
- Only the run summary row stores SLA benchmark and final PASS/FAIL based on average time.

## Configuration

Core runtime settings are in `salesforce_tab_performance/config.py`:

- `ITERATIONS`
- `SLA_SECONDS`
- `STABILIZATION_WAIT`
- default start/end XPaths
- family-specific end locators (metro areas, reports, custom dashboards)

## Contributing

See `CONTRIBUTING.md` for branch, testing, and PR guidance.

## CI/CD (Jenkins)

This repository includes a root `Jenkinsfile` with a professional, parameterized pipeline.

- Local Jenkins setup guide: `docs/JENKINS_SETUP.md`
- Supports modes: `ALL_TABS`, `SMOKE`, and `CHECKBOX_SELECTION`
- Archives JUnit + Allure + Excel artifacts

## License

This project is licensed under the MIT License. See `LICENSE`.
