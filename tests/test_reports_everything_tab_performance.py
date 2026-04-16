"""Performance test for Reports Everything tab."""

import allure

from salesforce_tab_performance.config import REPORTS_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

REPORTS_EVERYTHING_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/report/Report/Recent/Report/?queryScope=everything"
REPORTS_EVERYTHING_TAB_NAME = "Reports Everything"
@allure.feature("Salesforce Tab Performance")
@allure.story("Reports Everything Tab Component Render Completion")
def test_reports_everything_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=REPORTS_EVERYTHING_TAB_NAME,
        tab_url=REPORTS_EVERYTHING_TAB_URL,
        end_element_xpath=REPORTS_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
