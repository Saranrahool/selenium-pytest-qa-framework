# Test Plan - Fleet Device Portal

## 1. Objective
Verify that the Fleet Device Portal meets requirements REQ-01 to REQ-06 (see [REQUIREMENTS.md](REQUIREMENTS.md)) before release, and catch regressions automatically on every change.

## 2. Scope
**In scope**
- Sign-in, sign-out and session handling
- Device list, status filter and search
- Device configuration form and its input validation

**Out of scope**
- Performance and load testing
- Cross-browser testing (Chrome only for this release)
- Back-end APIs (the demo app has no server-side logic)

## 3. Approach
| Level | What | How |
|-------|------|-----|
| Functional | Each requirement, positive and negative paths | Automated UI tests, Selenium + pytest |
| Input validation | Retention days | Boundary value analysis (0, 1, 2, 89, 90, 91) plus invalid types |
| Input validation | IP address | Equivalence partitioning (valid, out of range, wrong format, empty) |
| Regression | Full suite | Runs in GitHub Actions on every push and pull request |
| Smoke | Critical paths only | `pytest -m smoke` for a fast check |

Tests use the **Page Object Model**, so locators live in one place (`pages/`) and tests read like the test cases.
Each test starts a fresh browser session, so tests are independent and can run in any order.

## 4. Environment
- Python 3.11+, Selenium 4, pytest 8
- Chrome (headless by default; set `HEADED=1` to watch)
- The app is served locally by a pytest fixture, so no external setup is needed

## 5. Entry and exit criteria
**Entry:** build available, requirements reviewed, test environment runs.
**Exit:** all planned test cases executed; no open Critical or High defects; any known Medium/Low defects documented and tracked with an expected-failure test.

## 6. Deliverables
- [Test cases](TEST_CASES.md)
- [Traceability matrix](TRACEABILITY.md)
- [Defect reports](bugs/)
- HTML test report and failure screenshots (CI artifacts)

## 7. Defect severity
| Severity | Meaning |
|----------|---------|
| Critical | Blocks a core workflow, no workaround |
| High | Major function broken, poor workaround |
| Medium | Function works incorrectly, workaround exists |
| Low | Cosmetic or minor inconvenience |

## 8. Risks
| Risk | Mitigation |
|------|------------|
| Flaky UI timing | Explicit waits only, no fixed sleeps |
| Browser/driver version drift | Selenium Manager resolves the driver automatically |
| Test data coupling | Fixed seed data in `app/app.js`; tests assert exact expected values |
