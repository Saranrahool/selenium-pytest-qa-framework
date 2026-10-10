# Test Cases

| ID | Requirement | Title | Steps | Expected result | Automated in |
|----|-------------|-------|-------|-----------------|--------------|
| TC-001 | REQ-01 | Valid sign-in | Sign in as `tester` / `Passw0rd!` | Device list opens and shows "tester" | `test_login.py::test_valid_login_opens_device_list` |
| TC-002 | REQ-01 | Wrong password | Sign in as `tester` with a wrong password | "Invalid username or password." and stays on sign-in | `test_login.py::test_invalid_credentials_are_rejected` |
| TC-003 | REQ-01 | Unknown user | Sign in as `nobody` | Same generic error (no hint whether the user exists) | `test_login.py::test_invalid_credentials_are_rejected` |
| TC-004 | REQ-01 | Required fields | Submit with username, password or both empty | "Username and password are required." | `test_login.py::test_required_fields` |
| TC-005 | REQ-01 | Locked account | Sign in as `locked_user` with the correct password | Locked-account message, stays on sign-in | `test_login.py::test_locked_account_cannot_sign_in` |
| TC-006 | REQ-02 | Direct access without session | Open `devices.html` without signing in | Redirected to sign-in | `test_login.py::test_device_list_requires_login` |
| TC-007 | REQ-02 | Sign-out | Sign in, sign out, reopen `devices.html` | Redirected to sign-in | `test_login.py::test_logout_ends_session` |
| TC-008 | REQ-03 | Default list | Sign in | All 6 devices, "6 device(s)" | `test_device_list.py::test_all_devices_listed_by_default` |
| TC-009 | REQ-03 | Status filter | Filter Online, then Offline | Only matching statuses (4 and 2) | `test_device_list.py::test_status_filter` |
| TC-010 | REQ-03 | Search by bus | Search "Bus 214" | CAM-1101, NVR-2101 | `test_device_list.py::test_search_by_bus` |
| TC-011 | REQ-03 | Search by device ID | Search "NVR-2001" | NVR-2001 only | `test_device_list.py::test_search_by_device_id` |
| TC-012 | REQ-03 | Case-insensitive search | Search "bus 214" | CAM-1101, NVR-2101 | `test_device_list.py::test_search_is_case_insensitive` **(fails: BUG-001)** |
| TC-013 | REQ-03 | No results | Search "Bus 999" | Empty table, "0 device(s)" | `test_device_list.py::test_search_with_no_match` |
| TC-014 | REQ-03 | Filter + search | Filter Offline, search "Bus 101" | No results | `test_device_list.py::test_filter_and_search_combined` |
| TC-015 | REQ-04 | Open device | Click NVR-2101 in the list | Title and details match the device | `test_device_config.py::test_open_device_from_list` |
| TC-016 | REQ-04 | Unknown device | Open `device.html?id=CAM-0000` | "Device not found", form hidden | `test_device_config.py::test_unknown_device_shows_not_found` |
| TC-017 | REQ-06 | Retention boundaries | Save with 0, 1, 2, 89, 90, 91, -5, 30.5, abc, empty | 1-90 save; all others show the retention error | `test_device_config.py::test_retention_boundaries` |
| TC-018 | REQ-05 | IP validation | Save with valid and invalid IPv4 values | Valid saves; invalid shows the IP error | `test_device_config.py::test_ip_address_validation` |
| TC-019 | REQ-06 | Resolution required | Clear resolution and save | "Select a supported resolution." | `test_device_config.py::test_resolution_is_required` |
| TC-020 | REQ-06 | Valid save clears errors | Save invalid values, then valid ones | Confirmation shown, errors cleared | `test_device_config.py::test_valid_configuration_saves` |
