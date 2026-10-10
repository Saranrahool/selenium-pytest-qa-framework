# Requirements - Fleet Device Portal

The system under test is a small web portal for managing cameras and recorders installed on a bus fleet. It lives in [`app/`](../app).

| ID | Requirement |
|----|-------------|
| REQ-01 | Users sign in with a username and password. Missing fields, invalid credentials and locked accounts each show a clear error, and the user stays on the sign-in page. |
| REQ-02 | Device pages are only available to signed-in users. Signing out ends the session. |
| REQ-03 | The device list shows all devices with a result count, can be filtered by status (All, Online, Offline), and can be searched by bus name or device ID. Search is case-insensitive. |
| REQ-04 | Each device has a configuration page showing its type, bus and firmware. Unknown device IDs show "Device not found". |
| REQ-05 | The device IP address must be a valid IPv4 address (four numbers from 0 to 255). |
| REQ-06 | Video retention must be a whole number from 1 to 90 days, and a resolution (720p, 1080p, 4K) must be selected. A valid configuration saves and shows a confirmation. |
