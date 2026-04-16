"""Performance test for Fundraising News tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Fundraising News Tab Component Render Completion")
def test_fundraising_news_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Fundraising News",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/fundraising-news",
    )
