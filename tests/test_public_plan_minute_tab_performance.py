"""Performance test for Public Plan Minute tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Public Plan Minute Tab Component Render Completion")
def test_public_plan_minute_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Public Plan Minute",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/public-plan-minute/Public_Plan_Minute__c/Default",
    )
