"""Performance test for University Alumni tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("University Alumni Tab Component Render Completion")
def test_university_alumni_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="university_alumni",
    )
