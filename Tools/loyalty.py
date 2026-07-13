import json
import os
from typing import Dict

STATE_FILE = os.path.join(os.path.dirname(__file__), "loyalty_state.json")
DISCOUNT_RATE = 0.10
VISITS_PER_DISCOUNT = 3


def _reset_state_for_tests() -> None:
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)


def _load_state() -> Dict[str, Dict[str, int]]:
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_state(state: Dict[str, Dict[str, int]]) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


def record_visit(customer_id: str) -> Dict[str, int]:
    """Record a new visit and grant a discount reward every 3 visits."""
    state = _load_state()
    customer_state = state.setdefault(customer_id, {"visits": 0, "available_discounts": 0})
    customer_state["visits"] += 1

    if customer_state["visits"] % VISITS_PER_DISCOUNT == 0:
        customer_state["available_discounts"] += 1

    _save_state(state)
    return customer_state


def get_loyalty_status(customer_id: str) -> Dict[str, int | bool]:
    """Return visit count and whether a discount is currently available."""
    state = _load_state()
    customer_state = state.get(customer_id, {"visits": 0, "available_discounts": 0})
    return {
        "visits": customer_state.get("visits", 0),
        "available_discounts": customer_state.get("available_discounts", 0),
        "discount_available": customer_state.get("available_discounts", 0) > 0,
    }


def redeem_discount(customer_id: str, bill_amount: float) -> str:
    """Redeem one available discount, if any."""
    state = _load_state()
    customer_state = state.get(customer_id)
    if not customer_state or customer_state.get("available_discounts", 0) <= 0:
        return "No discount available yet. Keep visiting to earn rewards."

    discount_amount = bill_amount * DISCOUNT_RATE
    final_amount = bill_amount - discount_amount
    customer_state["available_discounts"] -= 1
    _save_state(state)
    return f"10% loyalty discount applied. You saved {discount_amount:.2f} EGP. Final amount: {final_amount:.2f} EGP."


__all__ = [
    "DISCOUNT_RATE",
    "VISITS_PER_DISCOUNT",
    "record_visit",
    "get_loyalty_status",
    "redeem_discount",
    "_reset_state_for_tests",
]
