"""Shared runner for Salesforce tab performance tests."""

from __future__ import annotations

import time
from statistics import mean

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from . import config
from .credentials_utils import get_credential
from .excel_logger import log_performance_results
from .performance_utils import measure_component_render_time


def run_tab_performance_test(
    driver,
    tab_name: str,
    tab_url: str,
    start_element_xpath: str | None = None,
    end_element_xpath: str | None = None,
    end_condition: str = "visible",
) -> None:
    """Run login, navigate to tab, measure render times, and assert SLA."""
    wait = WebDriverWait(driver, 30)

    with allure.step("Open login page and authenticate"):
        _login_to_salesforce(driver, wait)

    with allure.step(f"Open {tab_name} tab URL directly"):
        driver.get(tab_url)

    with allure.step(f"Stabilize for {config.STABILIZATION_WAIT} seconds before measurement"):
        time.sleep(config.STABILIZATION_WAIT)

    execution_times = []
    with allure.step(f"Measure render completion for {config.ITERATIONS} iterations"):
        for iteration in range(1, config.ITERATIONS + 1):
            driver.refresh()
            duration = measure_component_render_time(
                driver,
                start_element_xpath=start_element_xpath,
                end_element_xpath=end_element_xpath,
                end_condition=end_condition,
            )
            execution_times.append(duration)
            allure.attach(
                body=f"Iteration {iteration}: {duration:.3f} seconds",
                name=f"Iteration {iteration} Result",
                attachment_type=allure.attachment_type.TEXT,
            )

    average_time = round(mean(execution_times), 3)
    sla_status = "PASS" if average_time <= config.SLA_SECONDS else "FAIL"
    capabilities = driver.capabilities or {}
    browser_name = str(capabilities.get("browserName", "chrome")).title()
    browser_version = str(capabilities.get("browserVersion", "Unknown"))
    browser_label = f"{browser_name} {browser_version}"
    platform = str(
        capabilities.get("platformName")
        or capabilities.get("platform")
        or capabilities.get("os")
        or "Unknown"
    )
    os_version = str(
        capabilities.get("osVersion")
        or capabilities.get("platformVersion")
        or "Unknown"
    )

    with allure.step("Write iteration and average results to Excel"):
        excel_path = log_performance_results(
            tab_name=tab_name,
            execution_times=execution_times,
            average_time=average_time,
            sla_seconds=config.SLA_SECONDS,
            browser=browser_label,
            platform=platform,
            os_version=os_version,
        )
        allure.attach(
            body=f"Results saved to: {excel_path}",
            name="Excel Output Path",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Attach final performance summary"):
        summary = (
            f"Tab Name: {tab_name}\n"
            f"Iterations: {config.ITERATIONS}\n"
            f"Execution Times: {execution_times}\n"
            f"Average Time: {average_time:.3f} seconds\n"
            f"SLA Threshold: {config.SLA_SECONDS:.3f} seconds\n"
            f"SLA Status: {sla_status}"
        )
        allure.attach(
            body=summary,
            name="Performance Summary",
            attachment_type=allure.attachment_type.TEXT,
        )

    assert average_time <= config.SLA_SECONDS, (
        f"{tab_name} average render time {average_time:.3f}s exceeded SLA "
        f"{config.SLA_SECONDS:.3f}s"
    )


def _login_to_salesforce(driver, wait: WebDriverWait) -> None:
    """Authenticate with credentials provided via environment variables."""
    username = _required_env("SF_USERNAME")
    password = _required_env("SF_PASSWORD")

    driver.get(config.LOGIN_URL)
    wait.until(ec.visibility_of_element_located((By.ID, config.USERNAME_FIELD_ID))).send_keys(username)
    wait.until(ec.visibility_of_element_located((By.ID, config.PASSWORD_FIELD_ID))).send_keys(password)
    wait.until(ec.element_to_be_clickable((By.ID, config.SUBMIT_BUTTON_ID))).click()
    wait.until(ec.visibility_of_element_located((By.XPATH, config.START_ELEMENT_XPATH)))


def _required_env(variable_name: str) -> str:
    """Fail clearly if required credential variable is missing."""
    value = get_credential(variable_name)
    if not value:
        pytest.fail(
            f"Missing required environment variable: {variable_name}. "
            "Set it via setx, current shell env, or .env in project root."
        )
    return value
