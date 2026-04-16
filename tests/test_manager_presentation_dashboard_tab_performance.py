"""Performance test for Manager Presentation Dashboard tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Manager Presentation Dashboard Tab Component Render Completion")
def test_manager_presentation_dashboard_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Manager Presentation Dashboard",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/manager-presentation-dashboard",
    )
