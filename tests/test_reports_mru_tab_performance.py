"""Performance test for Reports MRU tab."""

import allure

from salesforce_tab_performance.config import REPORTS_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

REPORTS_MRU_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/report/Report/Recent/Report/?queryScope=mru"
REPORTS_MRU_TAB_NAME = "Reports MRU"
@allure.feature("Salesforce Tab Performance")
@allure.story("Reports MRU Tab Component Render Completion")
def test_reports_mru_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=REPORTS_MRU_TAB_NAME,
        tab_url=REPORTS_MRU_TAB_URL,
        end_element_xpath=REPORTS_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
