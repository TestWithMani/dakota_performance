"""Performance test for Marketplace Searches tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Marketplace Searches Tab Component Render Completion")
def test_marketplace_searches_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Marketplace Searches",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/marketplace-searches/Marketplace_Searches__c/Default",
    )
