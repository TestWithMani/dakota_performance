"""Pytest fixtures for Selenium driver lifecycle."""

from __future__ import annotations

import sys
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from salesforce_tab_performance.credentials_utils import bootstrap_credentials

SMOKE_TEST_FILES = {
    "test_accounts_tab_performance.py",
    "test_all_documents_tab_performance.py",
    "test_13f_filings_tab_performance.py",
    "test_contact_tab_performance.py",
    "test_marketplace_home_tab_performance.py",
    "test_portfolio_companies_tab_performance.py",
    "test_public_company_search_tab_performance.py",
}


@pytest.fixture(scope="session", autouse=True)
def preload_credentials() -> None:
    """Load persisted credentials before any tests execute."""
    bootstrap_credentials()


@pytest.fixture(scope="function")
def driver():
    """Provide a clean Chrome WebDriver instance for each test."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-gpu")

    # Selenium Manager resolves ChromeDriver automatically for Selenium 4.6+.
    service = Service()
    web_driver = webdriver.Chrome(service=service, options=chrome_options)
    web_driver.implicitly_wait(0)
    yield web_driver
    try:
        web_driver.quit()
    except Exception:
        # Browser process may already be gone for crashed/disconnected sessions.
        pass


def pytest_collection_modifyitems(items):
    """Auto-tag tests by category and smoke suite."""
    for item in items:
        file_name = Path(item.fspath).name.lower()

        item.add_marker(pytest.mark.full)

        if file_name in SMOKE_TEST_FILES:
            item.add_marker(pytest.mark.smoke)

        if "home_tab" in file_name:
            item.add_marker(pytest.mark.Test)

        if "contact" in file_name:
            item.add_marker(pytest.mark.contacts)

        if "account" in file_name:
            item.add_marker(pytest.mark.accounts)

        if any(token in file_name for token in ("document", "memo")):
            item.add_marker(pytest.mark.documents)

        if "transaction" in file_name:
            item.add_marker(pytest.mark.transactions)

        if "metro_area" in file_name or "metro_areas" in file_name:
            item.add_marker(pytest.mark.metro_areas)

        if "report" in file_name or "reports" in file_name:
            item.add_marker(pytest.mark.reports)

        if "dashboard" in file_name:
            item.add_marker(pytest.mark.custom_dashboards)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach browser diagnostics to Allure when test execution fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    try:
        allure.attach(
            body=driver.current_url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception:
        pass

    try:
        allure.attach(
            body=driver.page_source,
            name="Page Source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception:
        pass

    try:
        allure.attach(
            body=driver.get_screenshot_as_png(),
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass
