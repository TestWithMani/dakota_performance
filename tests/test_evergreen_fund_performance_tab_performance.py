"""Performance test for Evergreen Fund Performance tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Evergreen Fund Performance Tab Component Render Completion")
def test_evergreen_fund_performance_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Evergreen Fund Performance",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/evergreen-fund-performance",
    )
