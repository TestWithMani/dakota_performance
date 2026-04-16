# Contributing Guide

Thanks for contributing to the Dakota Marketplace Performance Suite.

## Development Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r salesforce_tab_performance/requirements.txt
```

Set required credentials:

- `SF_USERNAME`
- `SF_PASSWORD`

## Branch and PR Workflow

1. Create a feature branch from `main`.
2. Keep changes focused and scoped.
3. Run relevant tests locally before opening a PR.
4. Include clear PR summary and test evidence.

## Test Commands

```bash
pytest -q
pytest -q -m smoke
pytest -q --collect-only
```

## Coding Guidelines

- Keep shared logic in `salesforce_tab_performance/`.
- Keep tab-specific behavior in `tests/test_*`.
- Prefer configurable XPaths and conditions over hardcoded branching.
- Maintain deterministic output formatting in Excel logs.

## Commit Message Style

Use concise, intention-focused messages, for example:

- `Add clickable end-condition support for Home tab`
- `Map reports tests to reports marker`
- `Refine Excel summary SLA evaluation`
