"""Performance test for Investment Firm Metro Area tab."""

import allure

from salesforce_tab_performance.config import METRO_AREA_END_ELEMENT_XPATH
from salesforce_tab_performance.tab_test_runner import run_tab_performance_test

INVESTMENT_FIRM_METRO_AREA_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/investment-firm-metro-area"
INVESTMENT_FIRM_METRO_AREA_TAB_NAME = "Investment Firm Metro Area"


@allure.feature("Salesforce Tab Performance")
@allure.story("Investment Firm Metro Area Tab Component Render Completion")
def test_investment_firm_metro_area_tab_render_performance(driver):
    run_tab_performance_test(
        driver,
        tab_name=INVESTMENT_FIRM_METRO_AREA_TAB_NAME,
        tab_url=INVESTMENT_FIRM_METRO_AREA_TAB_URL,
        end_element_xpath=METRO_AREA_END_ELEMENT_XPATH,
        end_condition="clickable",
    )
