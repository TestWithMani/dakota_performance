"""Performance test for All Documents tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("All Documents Tab Component Render Completion")
def test_all_documents_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="All Documents",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/all-documents",
    )
