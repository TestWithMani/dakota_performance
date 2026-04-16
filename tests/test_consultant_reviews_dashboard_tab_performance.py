"""Performance test for Consultant Reviews Dashboard tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Consultant Reviews Dashboard Tab Component Render Completion")
def test_consultant_reviews_dashboard_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Consultant Reviews Dashboard",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/consultant-reviews-dashboard",
    )
