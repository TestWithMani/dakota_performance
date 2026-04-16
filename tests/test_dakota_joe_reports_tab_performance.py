"""Performance test for Dakota Joe Reports tab."""

import allure

from salesforce_tab_performance.config import REPORTS_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

DAKOTA_JOE_REPORTS_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/dakota-joe-reports"
DAKOTA_JOE_REPORTS_TAB_NAME = "Dakota Joe Reports"


@allure.feature("Salesforce Tab Performance")
@allure.story("Dakota Joe Reports Tab Component Render Completion")
def test_dakota_joe_reports_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=DAKOTA_JOE_REPORTS_TAB_NAME,
        tab_url=DAKOTA_JOE_REPORTS_TAB_URL,
        end_element_xpath=REPORTS_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
