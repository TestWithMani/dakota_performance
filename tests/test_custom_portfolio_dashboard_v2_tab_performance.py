"""Performance test for Custom Portfolio Dashboard (URL variant) tab."""

import allure

from salesforce_tab_performance.config import CUSTOM_DASHBOARD_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

CUSTOM_PORTFOLIO_DASHBOARD_V2_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/custom-portfolio-dashboard"
CUSTOM_PORTFOLIO_DASHBOARD_V2_TAB_NAME = "Custom Portfolio Dashboard"


@allure.feature("Salesforce Tab Performance")
@allure.story("Custom Portfolio Dashboard URL Variant Tab Component Render Completion")
def test_custom_portfolio_dashboard_v2_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=CUSTOM_PORTFOLIO_DASHBOARD_V2_TAB_NAME,
        tab_url=CUSTOM_PORTFOLIO_DASHBOARD_V2_TAB_URL,
        end_element_xpath=CUSTOM_DASHBOARD_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
