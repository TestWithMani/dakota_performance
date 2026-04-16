"""Performance test for Contact tab."""

import allure

from salesforce_tab_performance.tab_test_runner import run_tab_performance_test


@allure.feature("Salesforce Tab Performance")
@allure.story("Contact Tab Component Render Completion")
def test_contact_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name="Contact",
        tab_url="https://dakotanetworks.my.site.com/dakotaMarketplace/s/contact/Contact/Default",
    )
