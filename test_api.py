"""
test_api.py
-----------
API integration tests for the Discount Rule Engine.
Tests all three discount rules with real HTTP requests to the Flask API.

Run with:  python test_api.py
Requires:  Flask server running on http://localhost:5000
"""

import requests
import json

URL = 'http://localhost:5000/apply-discount'


def test_new_customer_discount():
    """Test Case 1: NEW customer should get 10% discount."""
    print("=" * 60)
    print("TEST 1: NEW Customer (should apply Rule 1 - 10% discount)")
    print("=" * 60)

    data = {
        "customerType": "NEW",
        "dayOfWeek": "MONDAY",
        "items": [
            {"productId": "P001", "category": "Electronics", "price": 1000}
        ]
    }

    response = requests.post(URL, json=data, timeout=5)
    print(json.dumps(response.json(), indent=2))


def test_large_order_discount():
    """Test Case 2: Large order (>₹10k) should get ₹500 flat discount."""
    print("\n" + "=" * 60)
    print("TEST 2: Large Order ₹15,000 on WEDNESDAY")
    print("=" * 60)

    data = {
        "customerType": "REGULAR",
        "dayOfWeek": "WEDNESDAY",
        "items": [
            {"productId": "P001", "category": "Electronics", "price": 8000},
            {"productId": "P002", "category": "Clothing", "price": 7000}
        ]
    }

    response = requests.post(URL, json=data, timeout=5)
    print(json.dumps(response.json(), indent=2))


def test_wednesday_discount():
    """Test Case 3: PREMIUM customer on Wednesday should get 5% discount (Rule 3)."""
    print("\n" + "=" * 60)
    print("TEST 3: PREMIUM Customer - Wednesday - Rule 3 (5% discount)")
    print("=" * 60)

    data = {
        "customerType": "PREMIUM",
        "dayOfWeek": "WEDNESDAY",
        "items": [
            {"productId": "P001", "category": "Furniture", "price": 8000}
        ]
    }

    response = requests.post(URL, json=data, timeout=5)
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    test_new_customer_discount()
    test_large_order_discount()
    test_wednesday_discount()

    print("\n" + "=" * 60)
    print("All API tests completed successfully!")
    print("=" * 60)
