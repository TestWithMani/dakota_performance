"""Performance test for University Alumni tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("University Alumni Tab Component Render Completion")
def test_university_alumni_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="University Alumni",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/university-alumni/University_Alumni__c/Default",
    )
