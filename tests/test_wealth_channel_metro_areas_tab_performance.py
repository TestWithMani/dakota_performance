"""Performance test for Wealth Channel Metro Areas tab."""

import allure

from salesforce_tab_performance.config import METRO_AREA_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

WEALTH_CHANNEL_METRO_AREAS_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/wealth-channel-metro-areas"
WEALTH_CHANNEL_METRO_AREAS_TAB_NAME = "Wealth Channel Metro Areas"


@allure.feature("Salesforce Tab Performance")
@allure.story("Wealth Channel Metro Areas Tab Component Render Completion")
def test_wealth_channel_metro_areas_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=WEALTH_CHANNEL_METRO_AREAS_TAB_NAME,
        tab_url=WEALTH_CHANNEL_METRO_AREAS_TAB_URL,
        end_element_xpath=METRO_AREA_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
