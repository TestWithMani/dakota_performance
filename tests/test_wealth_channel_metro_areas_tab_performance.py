"""Performance test for Wealth Channel Metro Areas tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Wealth Channel Metro Areas Tab Component Render Completion")
def test_wealth_channel_metro_areas_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="wealth_channel_metro_areas",
    )
