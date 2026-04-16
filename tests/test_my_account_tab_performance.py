"""Performance test for My Account tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("My Account Tab Component Render Completion")
def test_my_account_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="My Account",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/my-account/My_Account__c/Default",
    )
