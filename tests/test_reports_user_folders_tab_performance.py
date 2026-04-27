"""Performance test for Reports User Folders tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Reports User Folders Tab Component Render Completion")
def test_reports_user_folders_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="reports_user_folders",
    )
