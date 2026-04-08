"""
test_engine.py
--------------
Unit tests for the Discount Rule Engine.
Covers all 3 required scenarios + bonus edge cases.

Run with:  python test_engine.py
"""

import unittest
from discount_engine import (
    build_engine, Order, Item,
    CustomerType, DayOfWeek
)


class TestDiscountEngine(unittest.TestCase):

    def setUp(self):
        """Create a fresh engine before each test."""
        self.engine = build_engine()

    # ──────────────────────────────────────────
    # Required Test Cases
    # ──────────────────────────────────────────

    def test_case_1_new_customer_large_order_wednesday(self):
        """
        Scenario: New customer | ₹15,000 order | Wednesday
        Expected: Rule 1 wins (highest priority) → 10% of 15000 = ₹1500
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
        print(f"  [PASS] Test 1 PASSED — Rule 1 applied: {result.applied_rule}")

    def test_case_2_regular_customer_large_order_friday(self):
        """
        Scenario: Regular customer | ₹12,000 order | Friday
        Expected: Rule 2 applies (>₹10k) → flat ₹500 off
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
        print(f"  [PASS] Test 2 PASSED — Rule 2 applied: {result.applied_rule}")

    def test_case_3_premium_customer_small_order_wednesday(self):
        """
        Scenario: Premium customer | ₹8,000 order | Wednesday
        Expected: Rule 3 applies (only Wednesday matches) → 5% of 8000 = ₹400
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
        print(f"  [PASS] Test 3 PASSED — Rule 3 applied: {result.applied_rule}")

    # ──────────────────────────────────────────
    # Boundary Edge Case
    # ──────────────────────────────────────────

    def test_exact_boundary_10000(self):
        """
        Boundary test: ₹10,000 exactly should NOT trigger Rule 2.
        Rule 2 threshold is strictly > 10000, so 10000 exactly gets no discount.
        """
        order = Order(
            customer_type=CustomerType.REGULAR,
            items=[Item("P009", "Bags", 10000)],
            day_of_week=DayOfWeek.MONDAY
        )
        result = self.engine.apply(order)

        self.assertEqual(result.discount_amount, 0.0)   # ₹10,000 is not > ₹10,000
        print(f"  [PASS] Test 4 PASSED — Boundary ₹10,000 correctly excluded from Rule 2")


# ──────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*55)
    print("   RUNNING DISCOUNT ENGINE TEST SUITE")
    print("="*55 + "\n")

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDiscountEngine)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n" + "="*55)
        print(f"  [SUCCESS] ALL {result.testsRun} TESTS PASSED")
        print("="*55 + "\n")
    else:
        print(f"\n  [ERROR] {len(result.failures)} FAILED, {len(result.errors)} ERRORS")
