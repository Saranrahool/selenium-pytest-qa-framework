# Selenium + pytest QA Framework

[![UI tests](https://github.com/Saranrahool/selenium-pytest-qa-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/Saranrahool/selenium-pytest-qa-framework/actions/workflows/tests.yml)

An end-to-end UI test automation framework built with **Python, Selenium WebDriver and pytest**, covering the full QA workflow: requirements, test plan, test cases, traceability, automation, defect reporting and CI.

The system under test is a small **Fleet Device Portal** (in [`app/`](app)) for managing cameras and recorders on a bus fleet. It is bundled in the repo so the suite runs anywhere with no external dependencies, and it contains one real defect that the tests catch.

## What this project shows

| QA practice | Where |
|-------------|-------|
| Requirements with IDs | [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) |
| Test plan (scope, approach, entry/exit criteria, risks) | [docs/TEST_PLAN.md](docs/TEST_PLAN.md) |
| Test cases with steps and expected results | [docs/TEST_CASES.md](docs/TEST_CASES.md) |
| Requirements traceability matrix | [docs/TRACEABILITY.md](docs/TRACEABILITY.md) |
| Defect report with root cause | [docs/bugs/BUG-001.md](docs/bugs/BUG-001.md) |
| Page Object Model | [`pages/`](pages) |
| Boundary value analysis and equivalence partitioning | [`tests/test_device_config.py`](tests/test_device_config.py) |
| Screenshots on failure | [`conftest.py`](conftest.py) |
| CI with HTML/JUnit reports | [`.github/workflows/tests.yml`](.github/workflows/tests.yml) |

## Results
20 test cases → 39 automated test runs: **38 pass, 1 expected failure** (BUG-001, tracked with `xfail(strict=True)` so the suite flags it the moment the bug is fixed).

## Project structure
```
app/                     System under test (static HTML/JS)
pages/                   Page objects: one class per screen, all locators live here
tests/                   Test modules, one per feature area
docs/                    Requirements, test plan, test cases, traceability, bug reports
conftest.py              Local web server, WebDriver setup, failure screenshots
.github/workflows/       CI pipeline
```

## Running the tests
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                           # full suite (headless Chrome)
pytest -m smoke                  # critical paths only
HEADED=1 pytest                  # watch the browser
pytest --html=reports/report.html --self-contained-html
```
Requires Google Chrome. Selenium Manager downloads the matching driver automatically.

Optional environment variables: `CHROME_BINARY` (custom Chrome path), `CHROMEDRIVER` (custom driver path), `CHROMEDRIVER_ARGS` (extra driver flags).

## Design decisions
- **Explicit waits only.** No `time.sleep()`; every interaction waits for the element state it needs, which keeps the suite fast and stable.
- **Fresh browser per test.** Tests never share state, so they can run in any order.
- **Exact assertions.** Tests check the exact device IDs and messages expected, not just "something appeared".
- **Known bugs stay visible.** Instead of deleting or skipping a failing test, it is linked to a bug report and marked as an expected failure.

## Author
Rahool Saran · [rahoolsaran.com](https://rahoolsaran.com) · [LinkedIn](https://linkedin.com/in/rahool-saran)
