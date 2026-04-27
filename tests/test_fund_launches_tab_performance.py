"""Performance test for Fund Launches tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Fund Launches Tab Component Render Completion")
def test_fund_launches_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="fund_launches",
    )
