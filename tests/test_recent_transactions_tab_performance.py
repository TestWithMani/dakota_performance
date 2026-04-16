"""Performance test for Recent Transactions tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Recent Transactions Tab Component Render Completion")
def test_recent_transactions_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Recent Transactions",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/recent-transactions",
    )
