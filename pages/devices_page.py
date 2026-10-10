from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class DevicesPage(BasePage):
    path = "devices.html"

    HEADING = (By.TAG_NAME, "h1")
    CURRENT_USER = (By.ID, "current-user")
    LOGOUT = (By.ID, "logout-button")
    STATUS_FILTER = (By.ID, "status-filter")
    SEARCH = (By.ID, "search")
    ROWS = (By.CSS_SELECTOR, "#device-table tbody tr")
    RESULT_COUNT = (By.ID, "result-count")

    def wait_until_loaded(self):
        self.wait().until(EC.url_contains(self.path))
        self.find_visible(self.RESULT_COUNT)
        return self

    def filter_by_status(self, status):
        Select(self.find(self.STATUS_FILTER)).select_by_visible_text(status)

    def search(self, text):
        self.type(self.SEARCH, text)

    def device_ids(self):
        return [row.get_attribute("data-device-id") for row in self.driver.find_elements(*self.ROWS)]

    def statuses(self):
        return [row.find_element(By.CLASS_NAME, "status").text for row in self.driver.find_elements(*self.ROWS)]

    def result_count_text(self):
        return self.find(self.RESULT_COUNT).text

    def open_device(self, device_id):
        self.click((By.LINK_TEXT, device_id))

    def logout(self):
        self.click(self.LOGOUT)
