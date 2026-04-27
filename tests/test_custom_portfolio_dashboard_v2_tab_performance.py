"""Performance test for Custom Portfolio Dashboard (URL variant) tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Custom Portfolio Dashboard URL Variant Tab Component Render Completion")
def test_custom_portfolio_dashboard_v2_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="custom_portfolio_dashboard_v2",
    )
