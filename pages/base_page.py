"""Base page object with the explicit-wait helpers every page uses."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 5


class BasePage:
    path = ""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, query=""):
        self.driver.get(f"{self.base_url}/{self.path}{query}")
        return self

    def wait(self, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout)

    def find(self, locator):
        return self.wait().until(EC.presence_of_element_located(locator))

    def find_visible(self, locator):
        return self.wait().until(EC.visibility_of_element_located(locator))

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def click(self, locator):
        self.wait().until(EC.element_to_be_clickable(locator)).click()

    def is_visible(self, locator):
        elements = self.driver.find_elements(*locator)
        return bool(elements) and elements[0].is_displayed()

    @property
    def current_path(self):
        return self.driver.current_url.split("/")[-1].split("?")[0]
