"""Performance test for Private Fund Search tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Private Fund Search Tab Component Render Completion")
def test_private_fund_search_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Private Fund Search",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/private-fund-search-tab",
    )
