"""Performance test for Investment Allocator Metro Areas tab."""

import allure

from salesforce_tab_performance.config import METRO_AREA_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

INVESTMENT_ALLOCATOR_METRO_AREAS_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/investment-allocator-metro-areas"
INVESTMENT_ALLOCATOR_METRO_AREAS_TAB_NAME = "Investment Allocator Metro Areas"


@allure.feature("Salesforce Tab Performance")
@allure.story("Investment Allocator Metro Areas Tab Component Render Completion")
def test_investment_allocator_metro_areas_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=INVESTMENT_ALLOCATOR_METRO_AREAS_TAB_NAME,
        tab_url=INVESTMENT_ALLOCATOR_METRO_AREAS_TAB_URL,
        end_element_xpath=METRO_AREA_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
