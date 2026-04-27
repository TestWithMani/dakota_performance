"""Performance test for Dakota Joe Reports tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Dakota Joe Reports Tab Component Render Completion")
def test_dakota_joe_reports_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="dakota_joe_reports",
    )
