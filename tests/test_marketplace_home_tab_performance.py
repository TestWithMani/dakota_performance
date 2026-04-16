"""Performance test for Marketplace Home tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Marketplace Home Tab Component Render Completion")
def test_marketplace_home_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Marketplace Home",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/",
        end_element_xpath="(//button[@title='Click To Follow'])[1]",
        end_condition="clickable",
    )
