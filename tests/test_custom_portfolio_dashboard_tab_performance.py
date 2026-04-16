"""Performance test for Custom Portfolio Dashboard tab."""

import allure

from salesforce_tab_performance.config import CUSTOM_DASHBOARD_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Custom Portfolio Dashboard Tab Component Render Completion")
def test_custom_portfolio_dashboard_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Custom Portfolio Dashboard",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/custom-portfolio-dashboard",
        end_element_xpath=CUSTOM_DASHBOARD_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
