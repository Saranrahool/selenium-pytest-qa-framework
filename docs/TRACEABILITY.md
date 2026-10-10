# Requirements Traceability Matrix

Every requirement maps to at least one test case, and every test case maps to an automated test.

| Requirement | Test cases | Status |
|-------------|------------|--------|
| REQ-01 Sign-in and errors | TC-001, TC-002, TC-003, TC-004, TC-005 | Pass |
| REQ-02 Session protection | TC-006, TC-007 | Pass |
| REQ-03 Device list, filter, search | TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014 | **Fail: TC-012 ([BUG-001](bugs/BUG-001.md))** |
| REQ-04 Device details | TC-015, TC-016 | Pass |
| REQ-05 IP validation | TC-018 | Pass |
| REQ-06 Retention and resolution | TC-017, TC-019, TC-020 | Pass |

**Coverage:** 6 of 6 requirements covered, 20 test cases, 39 automated test runs (parametrized).
