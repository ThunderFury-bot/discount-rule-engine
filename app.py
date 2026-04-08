"""
app.py
------
Flask REST API for the Discount Rule Engine.

Endpoints:
  POST /apply-discount   → Apply discounts to an order
  GET  /rules            → List all active rules
  GET  /health           → Health check
"""

from flask import Flask, request, jsonify
from discount_engine import (
    build_engine, Order, Item,
    CustomerType, DayOfWeek
)

app = Flask(__name__)
engine = build_engine()


# ──────────────────────────────────────────────────
# Helper: Validate & Parse Incoming Order JSON
# ──────────────────────────────────────────────────

def parse_order(data: dict):
    """
    Validates request body and returns an Order object.
    Raises ValueError with a descriptive message on bad input.
    """
    errors = []

    # Validate customerType
    raw_customer = data.get("customerType", "").upper()
    if raw_customer not in CustomerType._value2member_map_:
        errors.append(f"Invalid customerType '{raw_customer}'. Must be one of: NEW, REGULAR, PREMIUM")

    # Validate dayOfWeek
    raw_day = data.get("dayOfWeek", "").upper()
    if raw_day not in DayOfWeek._value2member_map_:
        errors.append(f"Invalid dayOfWeek '{raw_day}'. Must be one of: MONDAY–SUNDAY")

    # Validate items
    raw_items = data.get("items", [])
    if not isinstance(raw_items, list) or len(raw_items) == 0:
        errors.append("'items' must be a non-empty list")

    if errors:
        raise ValueError(errors)

    # Parse items
    items = []
    for idx, item in enumerate(raw_items):
        for field in ["productId", "category", "price"]:
            if field not in item:
                errors.append(f"Item #{idx+1} is missing field '{field}'")
        if not errors:
            try:
                price = float(item["price"])
                if price < 0:
                    errors.append(f"Item #{idx+1} price cannot be negative")
            except (ValueError, TypeError):
                errors.append(f"Item #{idx+1} price must be a number")

    if errors:
        raise ValueError(errors)

    items = [
        Item(
            product_id=str(item["productId"]),
            category=str(item["category"]),
            price=float(item["price"])
        )
        for item in raw_items
    ]

    return Order(
        customer_type=CustomerType(raw_customer),
        items=items,
        day_of_week=DayOfWeek(raw_day)
    )


# ──────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────

@app.route("/apply-discount", methods=["POST"])
def apply_discount():
    """
    Apply discount rules to an order.

    Request body (JSON):
    {
        "customerType": "NEW",
        "dayOfWeek": "WEDNESDAY",
        "items": [
            { "productId": "P001", "category": "Electronics", "price": 8000 },
            { "productId": "P002", "category": "Clothing",    "price": 7000 }
        ]
    }

    Response (JSON):
    {
        "success": true,
        "order_total": 15000,
        "original_total": 15000,
        "discount_amount": 1500,
        "final_amount": 13500,
        "applied_rule": "Rule 1: New customer — 10% discount",
        "rule_priority": 1
    }
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"success": False, "errors": ["Request body must be valid JSON"]}), 400

    try:
        order = parse_order(data)
    except ValueError as e:
        return jsonify({"success": False, "errors": list(e.args[0])}), 400

    result = engine.apply(order)

    return jsonify({
        "success": True,
        "order_total": order.order_total,
        **result.to_dict()
    }), 200


@app.route("/rules", methods=["GET"])
def list_rules():
    """Returns all registered discount rules and their priorities."""
    rules_info = [
        {
            "priority": rule.priority,
            "name": rule.name
        }
        for rule in sorted(engine._rules, key=lambda r: r.priority)
    ]
    return jsonify({"success": True, "rules": rules_info}), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "Discount Rule Engine"}), 200


# ──────────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] Discount Rule Engine API starting...")
    print("   POST http://localhost:5000/apply-discount")
    print("   GET  http://localhost:5000/rules")
    print("   GET  http://localhost:5000/health\n")
    app.run(debug=True, port=5000)
