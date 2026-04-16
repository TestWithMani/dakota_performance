"""Performance test for Investment Firm Contacts tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Investment Firm Contacts Tab Component Render Completion")
def test_investment_firm_contacts_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Investment Firm Contacts",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/investment-firm-contacts",
    )
