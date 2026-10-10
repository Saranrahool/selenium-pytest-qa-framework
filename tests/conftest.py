import pytest

from pages.devices_page import DevicesPage
from pages.login_page import LoginPage


@pytest.fixture
def logged_in(driver, base_url):
    """Sign in as the standard test user and return the loaded device list page."""
    LoginPage(driver, base_url).open().login("tester", "Passw0rd!")
    return DevicesPage(driver, base_url).wait_until_loaded()
