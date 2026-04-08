"""
discount_engine.py
------------------
Pluggable Rule Engine for discount calculation.
Each rule is isolated, prioritised, and independently extensible.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from enum import Enum


# ──────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────

class CustomerType(str, Enum):
    NEW = "NEW"
    REGULAR = "REGULAR"
    PREMIUM = "PREMIUM"


class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


# ──────────────────────────────────────────────────
# Domain Models
# ──────────────────────────────────────────────────

@dataclass
class Item:
    product_id: str
    category: str
    price: float


@dataclass
class Order:
    customer_type: CustomerType
    items: List[Item]
    day_of_week: DayOfWeek

    @property
    def order_total(self) -> float:
        return round(sum(item.price for item in self.items), 2)


@dataclass
class DiscountResult:
    original_total: float
    discount_amount: float
    final_amount: float
    applied_rule: str
    rule_priority: int

    def to_dict(self) -> dict:
        return {
            "original_total": self.original_total,
            "discount_amount": self.discount_amount,
            "final_amount": self.final_amount,
            "applied_rule": self.applied_rule,
            "rule_priority": self.rule_priority
        }


# ──────────────────────────────────────────────────
# Abstract Base Rule
# ──────────────────────────────────────────────────

class DiscountRule(ABC):
    """
    Every discount rule must implement this interface.
    To add a new rule: create a subclass, implement all methods,
    and register it in build_engine().
    """

    @property
    @abstractmethod
    def priority(self) -> int:
        """Lower number = higher priority (1 is highest)."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable rule name for logging and response."""
        pass

    @abstractmethod
    def is_applicable(self, order: Order) -> bool:
        """Returns True if this rule qualifies for the given order."""
        pass

    @abstractmethod
    def calculate_discount(self, order: Order) -> float:
        """Returns the discount amount in ₹."""
        pass


# ──────────────────────────────────────────────────
# Concrete Rules
# ──────────────────────────────────────────────────

class NewCustomerRule(DiscountRule):
    """Rule 1 — New customers get 10% off. Highest priority."""

    @property
    def priority(self) -> int:
        return 1

    @property
    def name(self) -> str:
        return "Rule 1: New customer — 10% discount"

    def is_applicable(self, order: Order) -> bool:
        return order.customer_type == CustomerType.NEW

    def calculate_discount(self, order: Order) -> float:
        return round(order.order_total * 0.10, 2)


class LargeOrderRule(DiscountRule):
    """Rule 2 — Orders above ₹10,000 get flat ₹500 off."""

    THRESHOLD = 10_000.0
    FLAT_DISCOUNT = 500.0

    @property
    def priority(self) -> int:
        return 2

    @property
    def name(self) -> str:
        return "Rule 2: Large order (>₹10,000) — flat ₹500 discount"

    def is_applicable(self, order: Order) -> bool:
        return order.order_total > self.THRESHOLD

    def calculate_discount(self, order: Order) -> float:
        return self.FLAT_DISCOUNT


class WednesdayRule(DiscountRule):
    """Rule 3 — Wednesday orders get 5% off. Lowest priority."""

    @property
    def priority(self) -> int:
        return 3

    @property
    def name(self) -> str:
        return "Rule 3: Wednesday special — 5% discount"

    def is_applicable(self, order: Order) -> bool:
        return order.day_of_week == DayOfWeek.WEDNESDAY

    def calculate_discount(self, order: Order) -> float:
        return round(order.order_total * 0.05, 2)


# ──────────────────────────────────────────────────
# Rule Engine
# ──────────────────────────────────────────────────

class DiscountRuleEngine:
    """
    Evaluates all registered rules in priority order.
    Applies the single highest-priority applicable rule (Rule 4).
    """

    def __init__(self):
        self._rules: List[DiscountRule] = []

    def register(self, rule: DiscountRule) -> "DiscountRuleEngine":
        """Register a rule and keep the list sorted by priority."""
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority)
        return self  # Fluent API for chaining

    def apply(self, order: Order) -> DiscountResult:
        """Find the highest-priority applicable rule and apply it."""
        for rule in self._rules:
            if rule.is_applicable(order):
                discount = rule.calculate_discount(order)
                return DiscountResult(
                    original_total=order.order_total,
                    discount_amount=discount,
                    final_amount=round(order.order_total - discount, 2),
                    applied_rule=rule.name,
                    rule_priority=rule.priority
                )
        return DiscountResult(
            original_total=order.order_total,
            discount_amount=0.0,
            final_amount=order.order_total,
            applied_rule="No discount applicable",
            rule_priority=0
        )


# ──────────────────────────────────────────────────
# Engine Factory  ← Register all active rules here
# ──────────────────────────────────────────────────

def build_engine() -> DiscountRuleEngine:
    """
    Single place to register/deregister rules.
    To add a new rule: create the class above, then add it here.
    """
    return (
        DiscountRuleEngine()
        .register(NewCustomerRule())
        .register(LargeOrderRule())
        .register(WednesdayRule())
    )
