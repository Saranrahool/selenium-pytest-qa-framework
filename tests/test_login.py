"""Authentication and session tests. Covers REQ-01 and REQ-02."""
import pytest

from pages.devices_page import DevicesPage
from pages.login_page import LoginPage

VALID_USER = ("tester", "Passw0rd!")


@pytest.mark.smoke
def test_valid_login_opens_device_list(driver, base_url):
    """TC-001: A valid user is taken to the device list and their name is shown."""
    LoginPage(driver, base_url).open().login(*VALID_USER)
    devices = DevicesPage(driver, base_url).wait_until_loaded()
    assert devices.current_path == "devices.html"
    assert devices.find(DevicesPage.CURRENT_USER).text == "tester"


@pytest.mark.parametrize(
    "username, password",
    [("tester", "wrong-password"), ("nobody", "Passw0rd!")],
    ids=["TC-002-wrong-password", "TC-003-unknown-user"],
)
def test_invalid_credentials_are_rejected(driver, base_url, username, password):
    """TC-002, TC-003: Bad credentials show a generic error and stay on the login page."""
    page = LoginPage(driver, base_url).open()
    page.login(username, password)
    assert page.error_text() == "Invalid username or password."
    assert page.current_path == "index.html"


@pytest.mark.parametrize(
    "username, password",
    [("", "Passw0rd!"), ("tester", ""), ("", "")],
    ids=["missing-username", "missing-password", "both-missing"],
)
def test_required_fields(driver, base_url, username, password):
    """TC-004: Username and password are both required."""
    page = LoginPage(driver, base_url).open()
    page.login(username, password)
    assert page.error_text() == "Username and password are required."


def test_locked_account_cannot_sign_in(driver, base_url):
    """TC-005: A locked account gets a clear message even with the right password."""
    page = LoginPage(driver, base_url).open()
    page.login("locked_user", "Passw0rd!")
    assert "locked" in page.error_text().lower()
    assert page.current_path == "index.html"


@pytest.mark.smoke
def test_device_list_requires_login(driver, base_url):
    """TC-006: Opening the device list without a session redirects to sign-in."""
    DevicesPage(driver, base_url).open()
    login = LoginPage(driver, base_url)
    login.find_visible(LoginPage.USERNAME)
    assert login.current_path == "index.html"


def test_logout_ends_session(driver, base_url):
    """TC-007: After signing out, the device list is no longer reachable."""
    LoginPage(driver, base_url).open().login(*VALID_USER)
    devices = DevicesPage(driver, base_url).wait_until_loaded()
    devices.logout()
    LoginPage(driver, base_url).find_visible(LoginPage.USERNAME)

    devices.open()
    LoginPage(driver, base_url).find_visible(LoginPage.USERNAME)
    assert devices.current_path == "index.html"
