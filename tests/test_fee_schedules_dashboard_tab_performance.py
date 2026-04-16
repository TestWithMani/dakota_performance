"""Performance test for Fee Schedules Dashboard tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Fee Schedules Dashboard Tab Component Render Completion")
def test_fee_schedules_dashboard_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Fee Schedules Dashboard",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/fee-schedules-dashboard",
    )
