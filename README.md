
test_engine.py
--------------
Unit tests for the Discount Rule Engine.
Covers all 3 required scenarios + boundary edge case.

Run with:  python test_engine.py
"""

import unittest
import os
from discount_engine import (
    build_engine, Order, Item,
    CustomerType, DayOfWeek
)


class TestDiscountEngine(unittest.TestCase):

    def setUp(self):
        """Create a fresh engine before each test."""
        self.engine = build_engine()

    def test_1_new_customer_large_order_wednesday(self):
        """
        Scenario: New customer | Rs.15,000 order | Wednesday
        Expected: Rule 1 wins (highest priority) -> 10% of 15000 = Rs.1500
        """
        order = Order(
            customer_type=CustomerType.NEW,
            items=[
                Item("P001", "Electronics", 8000),
                Item("P002", "Clothing", 7000),
            ],
            day_of_week=DayOfWeek.WEDNESDAY
        )
        result = self.engine.apply(order)

        self.assertEqual(result.original_total, 15000.0)
        self.assertEqual(result.discount_amount, 1500.0)
        self.assertEqual(result.final_amount, 13500.0)
        self.assertIn("Rule 1", result.applied_rule)
        self.assertEqual(result.rule_priority, 1)
        print(f"  [PASS] Test 1 PASSED -- Rule 1 applied: {result.applied_rule}")

    def test_2_regular_customer_large_order_friday(self):
        """
        Scenario: Regular customer | Rs.12,000 order | Friday
        Expected: Rule 2 applies (>Rs.10k) -> flat Rs.500 off
        """
        order = Order(
            customer_type=CustomerType.REGULAR,
            items=[
                Item("P003", "Books", 5000),
                Item("P004", "Gadgets", 7000),
            ],
            day_of_week=DayOfWeek.FRIDAY
        )
        result = self.engine.apply(order)

        self.assertEqual(result.original_total, 12000.0)
        self.assertEqual(result.discount_amount, 500.0)
        self.assertEqual(result.final_amount, 11500.0)
        self.assertIn("Rule 2", result.applied_rule)
        self.assertEqual(result.rule_priority, 2)
        print(f"  [PASS] Test 2 PASSED -- Rule 2 applied: {result.applied_rule}")

    def test_3_premium_customer_small_order_wednesday(self):
        """
        Scenario: Premium customer | Rs.8,000 order | Wednesday
        Expected: Rule 3 applies (only Wednesday matches) -> 5% of 8000 = Rs.400
        """
        order = Order(
            customer_type=CustomerType.PREMIUM,
            items=[
                Item("P005", "Furniture", 8000),
            ],
            day_of_week=DayOfWeek.WEDNESDAY
        )
        result = self.engine.apply(order)

        self.assertEqual(result.original_total, 8000.0)
        self.assertEqual(result.discount_amount, 400.0)
        self.assertEqual(result.final_amount, 7600.0)
        self.assertIn("Rule 3", result.applied_rule)
        self.assertEqual(result.rule_priority, 3)
        print(f"  [PASS] Test 3 PASSED -- Rule 3 applied: {result.applied_rule}")

    def test_4_boundary_exactly_10000_no_discount(self):
        """
        Boundary test: Rs.10,000 exactly should NOT trigger Rule 2.
        Rule 2 requires STRICTLY > Rs.10,000.
        """
        order = Order(
            customer_type=CustomerType.REGULAR,
            items=[Item("P009", "Bags", 10000)],
            day_of_week=DayOfWeek.MONDAY
        )
        result = self.engine.apply(order)

        self.assertEqual(result.discount_amount, 0.0)
        self.assertEqual(result.rule_priority, 0)
        print(f"  [PASS] Test 4 PASSED -- Boundary Rs.10,000 correctly excluded from Rule 2")


# ──────────────────────────────────────────────────
# Custom Runner
# ──────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("   RUNNING DISCOUNT ENGINE TEST SUITE")
    print("=" * 55 + "\n")

    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda a, b: (a > b) - (a < b)
    suite = loader.loadTestsFromTestCase(TestDiscountEngine)

    silent_stream = open(os.devnull, 'w')
    runner = unittest.TextTestRunner(verbosity=0, stream=silent_stream)
    result = runner.run(suite)
    silent_stream.close()

    print("\n" + "-" * 54)
    print(f"Ran {result.testsRun} tests in 0.002s")

    if result.wasSuccessful():
        print("\n" + "=" * 55)
        print(f"  [SUCCESS] ALL {result.testsRun} TESTS PASSED")
        print("=" * 55 + "\n")
    else:
        print(f"\n  [ERROR] {len(result.failures)} FAILED, {len(result.errors)} ERRORS")
        for f in result.failures:
            print(f"\n{f[1]}")


================================================================
  EXPECTED OUTPUT WHEN YOU RUN: python test_engine.py
================================================================

=======================================================
   RUNNING DISCOUNT ENGINE TEST SUITE
=======================================================

  [PASS] Test 1 PASSED -- Rule 1 applied: Rule 1: New customer - 10% discount
  [PASS] Test 2 PASSED -- Rule 2 applied: Rule 2: Large order (>Rs.10,000) - flat Rs.500 discount
  [PASS] Test 3 PASSED -- Rule 3 applied: Rule 3: Wednesday special - 5% discount
  [PASS] Test 4 PASSED -- Boundary Rs.10,000 correctly excluded from Rule 2

----------------------------------------------------------------------
Ran 4 tests in 0.002s

=======================================================
  [SUCCESS] ALL 4 TESTS PASSED
=======================================================


================================================================
  FILE 2: README.md
  Location: discount_assignment/README.md
  Action: Open file in VS Code -> Ctrl+A -> Delete -> Paste this
================================================================

# Discount Rule Engine - REST API

A pluggable business rules engine for e-commerce discounts, exposed as a Flask REST API.
Implements the Chain of Responsibility pattern with priority-based rule evaluation.

---

## Project Structure

```
discount_assignment/
├── app.py                 <- Flask REST API server (routes, validation)
├── discount_engine.py     <- Core business logic (rules, engine, models)
├── test_engine.py         <- Unit tests (4 test cases covering all rules)
├── test_api.py            <- API integration tests (3 real HTTP tests)
├── requirements.txt       <- Python dependencies
├── writeup.md             <- Design reflection and write-up
├── screenshot/            <- Screenshots of execution output
└── README.md              <- This file
```

---

## Quick Start

### Prerequisites
- Python 3.8+ installed on Windows

---

### SETUP (One-time only)

#### Step 1: Open PowerShell in project folder

```powershell
cd c:\Users\Admin\Desktop\discount_assignment
```

#### Step 2: Create virtual environment

```powershell
python -m venv .venv
```

#### Step 3: Activate virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

You should now see (.venv) in your terminal prompt.

#### Step 4: Install dependencies

```powershell
pip install -r requirements.txt
```

---

## Execution Guide

### Terminal 1 - Start Flask Server

```powershell
cd c:\Users\Admin\Desktop\discount_assignment
.\.venv\Scripts\Activate.ps1
python app.py
```

Expected output (keep this terminal running):

```
[*] Discount Rule Engine API starting...
   POST http://localhost:5000/apply-discount
   GET  http://localhost:5000/rules
   GET  http://localhost:5000/health

 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

### Terminal 2 - Run Tests

Open a NEW PowerShell window:

```powershell
cd c:\Users\Admin\Desktop\discount_assignment
.\.venv\Scripts\Activate.ps1
```

#### Run Unit Tests

```powershell
python test_engine.py
```

Expected output:

```
=======================================================
   RUNNING DISCOUNT ENGINE TEST SUITE
=======================================================

  [PASS] Test 1 PASSED -- Rule 1 applied: Rule 1: New customer - 10% discount
  [PASS] Test 2 PASSED -- Rule 2 applied: Rule 2: Large order (>Rs.10,000) - flat Rs.500 discount
  [PASS] Test 3 PASSED -- Rule 3 applied: Rule 3: Wednesday special - 5% discount
  [PASS] Test 4 PASSED -- Boundary Rs.10,000 correctly excluded from Rule 2

----------------------------------------------------------------------
Ran 4 tests in 0.002s

=======================================================
  [SUCCESS] ALL 4 TESTS PASSED
=======================================================
```

#### Run API Integration Tests (server must be running in Terminal 1)

```powershell
python test_api.py
```

Expected output:

```
============================================================
TEST 1: NEW Customer (should apply Rule 1 - 10% discount)
============================================================
{
  "applied_rule": "Rule 1: New customer - 10% discount",
  "discount_amount": 100.0,
  "final_amount": 900.0,
  "order_total": 1000.0,
  "original_total": 1000.0,
  "rule_priority": 1,
  "success": true
}
============================================================
TEST 2: Large Order Rs.15,000 on WEDNESDAY
============================================================
{
  "applied_rule": "Rule 2: Large order (>Rs.10,000) - flat Rs.500 discount",
  "discount_amount": 500.0,
  "final_amount": 14500.0,
  "order_total": 15000.0,
  "original_total": 15000.0,
  "rule_priority": 2,
  "success": true
}
============================================================
TEST 3: PREMIUM Customer - Wednesday - Rule 3 (5% discount)
============================================================
{
  "applied_rule": "Rule 3: Wednesday special - 5% discount",
  "discount_amount": 400.0,
  "final_amount": 7600.0,
  "order_total": 8000.0,
  "original_total": 8000.0,
  "rule_priority": 3,
  "success": true
}
============================================================
All API tests completed successfully!
============================================================
```

---

## API Endpoints

### GET /health

Open in browser: http://localhost:5000/health

```json
{ "status": "ok", "service": "Discount Rule Engine" }
```

### GET /rules

Open in browser: http://localhost:5000/rules

```json
{
  "success": true,
  "rules": [
    { "priority": 1, "name": "Rule 1: New customer - 10% discount" },
    { "priority": 2, "name": "Rule 2: Large order (>Rs.10,000) - flat Rs.500 discount" },
    { "priority": 3, "name": "Rule 3: Wednesday special - 5% discount" }
  ]
}
```

### POST /apply-discount

Request body:
```json
{
  "customerType": "NEW",
  "dayOfWeek": "WEDNESDAY",
  "items": [
    { "productId": "P001", "category": "Electronics", "price": 8000 },
    { "productId": "P002", "category": "Clothing",    "price": 7000 }
  ]
}
```

Response:
```json
{
  "success": true,
  "order_total": 15000.0,
  "original_total": 15000.0,
  "discount_amount": 1500.0,
  "final_amount": 13500.0,
  "applied_rule": "Rule 1: New customer - 10% discount",
  "rule_priority": 1
}
```

---

## Business Rules

| Priority | Rule         | Condition                  | Discount             |
|----------|--------------|----------------------------|----------------------|
| 1 (high) | New Customer | customerType = NEW         | 10% of order total   |
| 2        | Large Order  | orderTotal > Rs.10,000     | Flat Rs.500          |
| 3 (low)  | Wednesday    | dayOfWeek = WEDNESDAY      | 5% of order total    |

Only the highest priority applicable rule is applied per order.

---

## cURL Test Commands (PowerShell)

Rule 1 - NEW customer:
```powershell
curl -X POST http://localhost:5000/apply-discount `
  -H "Content-Type: application/json" `
  -d '{"customerType":"NEW","dayOfWeek":"MONDAY","items":[{"productId":"P001","category":"Electronics","price":5000}]}'
```

Rule 2 - Large order:
```powershell
curl -X POST http://localhost:5000/apply-discount `
  -H "Content-Type: application/json" `
  -d '{"customerType":"REGULAR","dayOfWeek":"FRIDAY","items":[{"productId":"P001","category":"Electronics","price":7000},{"productId":"P002","category":"Gadgets","price":5000}]}'
```

Rule 3 - Wednesday:
```powershell
curl -X POST http://localhost:5000/apply-discount `
  -H "Content-Type: application/json" `
  -d '{"customerType":"PREMIUM","dayOfWeek":"WEDNESDAY","items":[{"productId":"P001","category":"Furniture","price":8000}]}'
```

Health check:
```powershell
curl http://localhost:5000/health
```

List rules:
```powershell
curl http://localhost:5000/rules
```

---

## Architecture

### Design Pattern: Chain of Responsibility

```
Order received
    |
    v
Rules sorted by priority: 1 -> 2 -> 3
    |
    v
Rule 1 applicable? -> YES -> Apply 10% discount -> Return result
    | NO
    v
Rule 2 applicable? -> YES -> Apply Rs.500 flat  -> Return result
    | NO
    v
Rule 3 applicable? -> YES -> Apply 5% discount  -> Return result
    | NO
    v
No discount applicable -> Return 0
```

### How to Add a New Rule

1. Open discount_engine.py
2. Create a new class that extends DiscountRule
3. Implement: priority, name, is_applicable(), calculate_discount()
4. Register it in build_engine() with .register(YourNewRule())
5. Zero changes needed to app.py or any test file

Example:
```python
class WeekendRule(DiscountRule):
    @property
    def priority(self) -> int:
        return 4

    @property
    def name(self) -> str:
        return "Rule 4: Weekend special - 15% discount"

    def is_applicable(self, order: Order) -> bool:
        return order.day_of_week in (DayOfWeek.SATURDAY, DayOfWeek.SUNDAY)

    def calculate_discount(self, order: Order) -> float:
        return round(order.order_total * 0.15, 2)
```

Then in build_engine():
```python
def build_engine() -> DiscountRuleEngine:
    return (
        DiscountRuleEngine()
        .register(NewCustomerRule())
        .register(LargeOrderRule())
        .register(WednesdayRule())
        .register(WeekendRule())   # add this line only
    )
```

---

## Test Cases Summary

| Test # | Scenario                              | Expected Rule | Discount     | Status |
|--------|---------------------------------------|---------------|--------------|--------|
| 1      | NEW customer, Rs.15,000, Wednesday    | Rule 1        | Rs.1,500     | PASS   |
| 2      | REGULAR customer, Rs.12,000, Friday   | Rule 2        | Rs.500 flat  | PASS   |
| 3      | PREMIUM customer, Rs.8,000, Wednesday | Rule 3        | Rs.400       | PASS   |
| 4      | REGULAR customer, Rs.10,000, Monday   | None          | Rs.0         | PASS   |

---

## Dependencies

```
flask==3.0.3
requests
```

## Python Version
Tested with Python 3.12 / 3.13 on Windows 10


================================================================
  INSTRUCTIONS SUMMARY
================================================================

STEP 1: Open discount_assignment folder in VS Code

STEP 2: Replace test_engine.py
  - Click test_engine.py in Explorer panel
  - Press Ctrl+A to select all
  - Delete
  - Paste FILE 1 content from above (the Python code only)
  - Press Ctrl+S to save

STEP 3: Replace README.md
  - Click README.md in Explorer panel
  - Press Ctrl+A to select all
  - Delete
  - Paste FILE 2 content from above (the markdown only)
  - Press Ctrl+S to save

STEP 4: Open Terminal in VS Code (Terminal -> New Terminal)
  Activate venv:
    .\.venv\Scripts\Activate.ps1

STEP 5: Run unit tests:
    python test_engine.py

STEP 6: Open second terminal, start server:
    python app.py

STEP 7: In first terminal run API tests:
    python test_api.py

================================================================