"""Performance test for Dakota Videos tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Dakota Videos Tab Component Render Completion")
def test_dakota_videos_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="dakota_videos",
    )
