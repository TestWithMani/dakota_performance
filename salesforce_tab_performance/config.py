"""Central configuration for Salesforce tab performance measurement."""

from pathlib import Path

LOGIN_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s"
ACCOUNTS_TAB_URL = "https://dakotanetworks.my.site.com/dakotaMarketplace/s/account/Account/Default"

# Keep this configurable so future tabs only require URL and tab name updates.
TAB_NAME = "Accounts"

ITERATIONS = 3
SLA_SECONDS = 15
STABILIZATION_WAIT = 5

# Login field identifiers
USERNAME_FIELD_ID = "loginPage:loginForm:login-email"
PASSWORD_FIELD_ID = "loginPage:loginForm:login-password"
SUBMIT_BUTTON_ID = "loginPage:loginForm:login-submit"

# Component render measurement locators
START_ELEMENT_XPATH = "//a[@title='Dakota Marketplace']"
END_ELEMENT_XPATH = "//tr[@class='slds-line-height_reset']"

# Metro area tab family: completion marker (clickable first parent container)
METRO_AREA_END_ELEMENT_XPATH = "(//div[@class='parentDiv'])[1]"

# Reports tab family: completion marker (clickable "Recent" nav item)
REPORTS_END_ELEMENT_XPATH = "//a[normalize-space()='Recent']"

# Custom dashboard tab family: completion marker (second table row clickable)
CUSTOM_DASHBOARD_END_ELEMENT_XPATH = "(//lightning-formatted-url[@data-navigation='enable'])[1]"

# Output
PROJECT_DIR = Path(__file__).resolve().parent
EXCEL_FILE_NAME = str(PROJECT_DIR / "performance_results.xlsx")
