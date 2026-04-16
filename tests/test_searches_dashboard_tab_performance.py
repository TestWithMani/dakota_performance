"""Performance test for Searches Dashboard tab."""

import allure

from salesforce_tab_performance.config import CUSTOM_DASHBOARD_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

SEARCHES_DASHBOARD_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/searches-dashboard"
SEARCHES_DASHBOARD_TAB_NAME = "Searches Dashboard"


@allure.feature("Salesforce Tab Performance")
@allure.story("Searches Dashboard Tab Component Render Completion")
def test_searches_dashboard_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=SEARCHES_DASHBOARD_TAB_NAME,
        tab_url=SEARCHES_DASHBOARD_TAB_URL,
        end_element_xpath=CUSTOM_DASHBOARD_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
