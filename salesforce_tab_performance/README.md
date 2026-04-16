# Salesforce Tab Performance

Lightweight Selenium + pytest + Allure framework to measure Salesforce Lightning component render completion time for Dakota Marketplace tabs.

## What This Measures

This project measures **component render completion time**, not browser page load:

- **Start:** when `//a[@title='Dakota Marketplace']` is visible
- **End:** when `//tr[@class='slds-line-height_reset']` is visible

Current target tab: `Accounts`.

## Project Structure

```text
salesforce_tab_performance/
├── config.py
├── performance_utils.py
├── excel_logger.py
├── test_accounts_tab_performance.py
├── conftest.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set Salesforce credentials (any one of these options):

```bash
# PowerShell
$env:SF_USERNAME="your_username"
$env:SF_PASSWORD="your_password"
```

Persistent option (recommended on Windows):

```bash
setx SF_USERNAME "your_username"
setx SF_PASSWORD "your_password"
```

Fallback option in project root (`salesforce_tab_performance/.env`):

```bash
SF_USERNAME=your_username
SF_PASSWORD=your_password
```

## Run Tests

```bash
pytest --alluredir=allure-results
```

## View Allure Report

```bash
allure serve allure-results
```

## Excel Output

Results are logged in `performance_results.xlsx` (auto-created if missing) with columns:

- `DateTime`
- `Tab Name`
- `Iteration`
- `Execution Time`
- `Average`
- `SLA Status`

## Future Tabs

To reuse this for another tab later, update only:

- `ACCOUNTS_TAB_URL` (or replace with your next tab URL)
- `TAB_NAME`

The same measurement flow and logging remain unchanged.
