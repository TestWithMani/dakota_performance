"""Performance test for Private Companies Transactions tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Private Companies Transactions Tab Component Render Completion")
def test_private_companies_transactions_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="private_companies_transactions",
    )
