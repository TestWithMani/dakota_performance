"""Performance test for Portfolio Companies Metro Area tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

@allure.feature("Salesforce Tab Performance")
@allure.story("Portfolio Companies Metro Area Tab Component Render Completion")
def test_portfolio_companies_metro_area_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_key="portfolio_companies_metro_area",
    )
