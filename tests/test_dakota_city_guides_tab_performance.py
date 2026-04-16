"""Performance test for Dakota City Guides tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Dakota City Guides Tab Component Render Completion")
def test_dakota_city_guides_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Dakota City Guides",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/dakota-city-guides",
    )
