"""Performance test for 13F Filings Investments Search tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("13F Filings Investments Search Tab Component Render Completion")
def test_13f_filings_investments_search_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="13f_filings_investments_search",
    )
