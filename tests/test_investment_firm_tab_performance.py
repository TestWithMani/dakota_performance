"""Performance test for Investment Firm tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

INVESTMENT_FIRM_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/investment-firm-list"
INVESTMENT_FIRM_TAB_NAME = "Investment Firm Accounts"


@allure.feature("Salesforce Tab Performance")
@allure.story("Investment Firm Tab Component Render Completion")
def test_investment_firm_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=INVESTMENT_FIRM_TAB_NAME,
        tab_url=INVESTMENT_FIRM_TAB_URL,
    )
