"""Performance test for Public Company Search tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Public Company Search Tab Component Render Completion")
def test_public_company_search_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="public_company_search",
    )
