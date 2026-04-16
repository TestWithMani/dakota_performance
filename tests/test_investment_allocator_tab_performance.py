"""Performance test for Investment Allocator tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

INVESTMENT_ALLOCATOR_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/investment-allocator-list"
INVESTMENT_ALLOCATOR_TAB_NAME = "Investment Allocator Accounts"


@allure.feature("Salesforce Tab Performance")
@allure.story("Investment Allocator Tab Component Render Completion")
def test_investment_allocator_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=INVESTMENT_ALLOCATOR_TAB_NAME,
        tab_url=INVESTMENT_ALLOCATOR_TAB_URL,
    )
