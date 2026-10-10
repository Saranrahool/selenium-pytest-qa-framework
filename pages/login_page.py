from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "index.html"

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "login-button")
    ERROR = (By.ID, "login-error")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def error_text(self):
        return self.find_visible(self.ERROR).text
