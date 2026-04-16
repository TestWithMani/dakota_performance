"""Performance test for Conference Dashboard tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

CONFERENCE_DASHBOARD_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/conference-dashboard"
CONFERENCE_DASHBOARD_TAB_NAME = "Conference Dashboard"


@allure.feature("Salesforce Tab Performance")
@allure.story("Conference Dashboard Tab Component Render Completion")
def test_conference_dashboard_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=CONFERENCE_DASHBOARD_TAB_NAME,
        tab_url=CONFERENCE_DASHBOARD_TAB_URL,
    )
