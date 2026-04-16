"""Utility helpers for measuring Lightning component render timing."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from . import config


def measure_component_render_time(
    driver: WebDriver,
    timeout: int = 30,
    start_element_xpath: str | None = None,
    end_element_xpath: str | None = None,
    end_condition: str = "visible",
) -> float:
    """
    Measure Salesforce Lightning component render completion time.

    Measurement rule:
    - Start time: when `Dakota Marketplace` anchor is visible.
    - End time: when the first row (`slds-line-height_reset`) is visible.
    """
    wait = WebDriverWait(driver, timeout)
    start_xpath = start_element_xpath or config.START_ELEMENT_XPATH
    end_xpath = end_element_xpath or config.END_ELEMENT_XPATH

    # Wait until the start marker is visible, then start timing immediately.
    wait.until(ec.visibility_of_element_located((By.XPATH, start_xpath)))
    start_time = time.perf_counter()

    # Wait for the tab-specific "ready" signal, then stop timing.
    if end_condition not in {"visible", "clickable"}:
        raise ValueError("end_condition must be either 'visible' or 'clickable'")

    if end_condition == "clickable":
        wait.until(ec.element_to_be_clickable((By.XPATH, end_xpath)))
    else:
        wait.until(ec.visibility_of_element_located((By.XPATH, end_xpath)))
    end_time = time.perf_counter()

    return round(end_time - start_time, 3)
