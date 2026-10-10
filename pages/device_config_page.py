from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class DeviceConfigPage(BasePage):
    path = "device.html"

    TITLE = (By.ID, "device-title")
    META = (By.ID, "device-meta")
    IP = (By.ID, "ip")
    RETENTION = (By.ID, "retention")
    RESOLUTION = (By.ID, "resolution")
    SAVE = (By.ID, "save-button")
    SUCCESS = (By.ID, "save-success")
    FORM = (By.ID, "config-form")

    def open_device(self, device_id):
        return self.open(f"?id={device_id}")

    def title(self):
        return self.find_visible(self.TITLE).text

    def fill(self, ip=None, retention=None, resolution=None):
        if ip is not None:
            self.type(self.IP, ip)
        if retention is not None:
            self.type(self.RETENTION, retention)
        if resolution is not None:
            Select(self.find(self.RESOLUTION)).select_by_value(resolution)

    def save(self):
        self.click(self.SAVE)

    def error_for(self, field):
        locator = (By.ID, f"{field}-error")
        return self.find(locator).text if self.is_visible(locator) else ""

    def saved_successfully(self):
        return self.is_visible(self.SUCCESS)
