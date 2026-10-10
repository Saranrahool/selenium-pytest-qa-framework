"""Device list, status filter and search tests. Covers REQ-03."""
import pytest

ALL_DEVICES = ["CAM-1001", "CAM-1002", "NVR-2001", "CAM-1101", "NVR-2101", "CAM-1201"]


@pytest.mark.smoke
def test_all_devices_listed_by_default(logged_in):
    """TC-008: With no filter, every device is listed and the count matches."""
    assert logged_in.device_ids() == ALL_DEVICES
    assert logged_in.result_count_text() == "6 device(s)"


@pytest.mark.parametrize("status, expected_count", [("Online", 4), ("Offline", 2)])
def test_status_filter(logged_in, status, expected_count):
    """TC-009: The status filter shows only devices with that status."""
    logged_in.filter_by_status(status)
    statuses = logged_in.statuses()
    assert len(statuses) == expected_count
    assert set(statuses) == {status}


def test_search_by_bus(logged_in):
    """TC-010: Searching by bus name returns only that bus's devices."""
    logged_in.search("Bus 214")
    assert logged_in.device_ids() == ["CAM-1101", "NVR-2101"]


def test_search_by_device_id(logged_in):
    """TC-011: Searching by device ID returns that single device."""
    logged_in.search("NVR-2001")
    assert logged_in.device_ids() == ["NVR-2001"]


@pytest.mark.xfail(strict=True, reason="BUG-001: device search is case-sensitive")
def test_search_is_case_insensitive(logged_in):
    """TC-012: Search should ignore case. Currently fails - see docs/bugs/BUG-001.md."""
    logged_in.search("bus 214")
    assert logged_in.device_ids() == ["CAM-1101", "NVR-2101"]


def test_search_with_no_match(logged_in):
    """TC-013: A search with no matches shows an empty table and a zero count."""
    logged_in.search("Bus 999")
    assert logged_in.device_ids() == []
    assert logged_in.result_count_text() == "0 device(s)"


def test_filter_and_search_combined(logged_in):
    """TC-014: Filter and search apply together (Bus 101 has no offline devices)."""
    logged_in.filter_by_status("Offline")
    logged_in.search("Bus 101")
    assert logged_in.device_ids() == []
