# Salesforce Tab Performance Module

Core implementation module for the Dakota Marketplace performance suite.

For complete setup and execution instructions, use the repository root guide:

- `../README.md`

## Module Contents

- `config.py`: test/runtime constants and reusable XPath locators
- `credentials_utils.py`: env, registry, and `.env` credential bootstrap
- `performance_utils.py`: timing helpers with `visible`/`clickable` end conditions
- `tab_test_runner.py`: shared test flow (login -> navigate -> iterate -> assert/log)
- `tabs_registry.py`: central tab key -> display name/url/end-condition metadata
- `excel_logger.py`: structured Excel output with run summary SLA evaluation

Update tab names, URLs, or special end locators in `tabs_registry.py`.

## Dependency Install

```bash
pip install -r salesforce_tab_performance/requirements.txt
```
