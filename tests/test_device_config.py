"""Device configuration form tests. Covers REQ-04, REQ-05 and REQ-06.

Uses boundary value analysis for retention days and equivalence
partitioning for IP addresses.
"""
import pytest

from pages.device_config_page import DeviceConfigPage


@pytest.fixture
def config_page(logged_in, driver, base_url):
    return DeviceConfigPage(driver, base_url).open_device("CAM-1001")


@pytest.mark.smoke
def test_open_device_from_list(logged_in, driver, base_url):
    """TC-015: Clicking a device opens its configuration page with the right details."""
    logged_in.open_device("NVR-2101")
    page = DeviceConfigPage(driver, base_url)
    assert page.title() == "NVR-2101"
    assert page.find(DeviceConfigPage.META).text == "Mobile recorder on Bus 214 (firmware 6.9.8)"


def test_unknown_device_shows_not_found(logged_in, driver, base_url):
    """TC-016: An unknown device ID shows 'Device not found' and hides the form."""
    page = DeviceConfigPage(driver, base_url).open_device("CAM-0000")
    assert page.title() == "Device not found"
    assert not page.is_visible(DeviceConfigPage.FORM)


@pytest.mark.parametrize(
    "retention, valid",
    [
        ("0", False),   # just below minimum
        ("1", True),    # minimum
        ("2", True),    # just above minimum
        ("89", True),   # just below maximum
        ("90", True),   # maximum
        ("91", False),  # just above maximum
        ("-5", False),  # negative
        ("30.5", False),  # not a whole number
        ("abc", False),  # not a number
        ("", False),    # empty
    ],
)
def test_retention_boundaries(config_page, retention, valid):
    """TC-017: Retention accepts whole numbers from 1 to 90 only."""
    config_page.fill(retention=retention)
    config_page.save()
    error = config_page.error_for("retention")
    if valid:
        assert error == ""
        assert config_page.saved_successfully()
    else:
        assert error == "Retention must be a whole number from 1 to 90 days."
        assert not config_page.saved_successfully()


@pytest.mark.parametrize(
    "ip, valid",
    [
        ("10.0.0.1", True),
        ("0.0.0.0", True),
        ("255.255.255.255", True),
        ("256.1.1.1", False),
        ("10.0.0", False),
        ("10.0.0.1.5", False),
        ("10.0.0.a", False),
        ("", False),
    ],
)
def test_ip_address_validation(config_page, ip, valid):
    """TC-018: Only valid IPv4 addresses are accepted."""
    config_page.fill(ip=ip)
    config_page.save()
    error = config_page.error_for("ip")
    assert (error == "") is valid
    assert config_page.saved_successfully() is valid


def test_resolution_is_required(config_page):
    """TC-019: Saving without a resolution shows an error."""
    config_page.fill(resolution="")
    config_page.save()
    assert config_page.error_for("resolution") == "Select a supported resolution."
    assert not config_page.saved_successfully()


@pytest.mark.smoke
def test_valid_configuration_saves(config_page):
    """TC-020: A fully valid configuration saves and clears earlier errors."""
    config_page.fill(ip="bad", retention="0")
    config_page.save()
    assert config_page.error_for("ip") and config_page.error_for("retention")

    config_page.fill(ip="172.16.5.20", retention="45", resolution="4K")
    config_page.save()
    assert config_page.saved_successfully()
    assert config_page.error_for("ip") == ""
    assert config_page.error_for("retention") == ""
