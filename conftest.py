"""Shared pytest fixtures: local app server, WebDriver setup, and screenshots on failure."""
import functools
import http.server
import os
import threading
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

APP_DIR = Path(__file__).parent / "app"
ARTIFACTS_DIR = Path(__file__).parent / "reports" / "screenshots"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def base_url():
    """Serve the demo app on a free localhost port for the whole test session."""
    handler = functools.partial(_QuietHandler, directory=str(APP_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def _chrome_options():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    if os.getenv("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]
    return options


@pytest.fixture
def driver():
    """A fresh Chrome session per test so tests never depend on each other."""
    service_args = os.getenv("CHROMEDRIVER_ARGS", "").split() or None
    service = Service(os.getenv("CHROMEDRIVER"), service_args=service_args)
    drv = webdriver.Chrome(service=service, options=_chrome_options())
    drv.implicitly_wait(0)  # explicit waits only, in the page objects
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot whenever a test fails, to make defects easier to characterize."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "driver" in item.fixturenames:
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        item.funcargs["driver"].save_screenshot(str(ARTIFACTS_DIR / f"{item.name}.png"))
