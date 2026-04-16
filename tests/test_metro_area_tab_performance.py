"""Performance test for Metro Area tab."""

import allure

from salesforce_tab_performance.config import METRO_AREA_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

METRO_AREA_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/metro-area/Metro_Area__c/Default"
METRO_AREA_TAB_NAME = "Metro Area"


@allure.feature("Salesforce Tab Performance")
@allure.story("Metro Area Tab Component Render Completion")
def test_metro_area_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=METRO_AREA_TAB_NAME,
        tab_url=METRO_AREA_TAB_URL,
        end_element_xpath=METRO_AREA_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
