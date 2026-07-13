import json
import os
from datetime import datetime
from typing import Dict

try:
    from langchain.tools import tool as langchain_tool
except ImportError:  # pragma: no cover - fallback for minimal environments
    def langchain_tool(name: str, description: str = "", return_direct: bool = False):
        def decorator(func):
            func.langchain_tool_name = name
            func.langchain_tool_description = description
            func.langchain_tool_return_direct = return_direct
            return func

        return decorator


tool = langchain_tool

LOCATIONS = [
    "Cairo",
    "Alexandria",
    "Giza",
    "Luxor",
    "Sharm El Sheikh",
]

TOTAL_TABLES = 50
STATE_FILE = os.path.join(os.path.dirname(__file__), "booking_state.json")


def _reset_state_for_tests() -> None:
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)


def _load_state() -> Dict[str, Dict[str, Dict[str, int]]]:
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_state(state: Dict[str, Dict[str, Dict[str, int]]]) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


def _normalize_location(location: str) -> str:
    normalized = location.strip().lower()
    mapping = {
        "cairo": "Cairo",
        "alexandria": "Alexandria",
        "giza": "Giza",
        "luxor": "Luxor",
        "sharm el sheikh": "Sharm El Sheikh",
        "sharm": "Sharm El Sheikh",
    }
    return mapping.get(normalized, location.strip().title())


def _validate_slot(time_slot: str) -> str:
    if not time_slot:
        raise ValueError("A time slot is required.")
    parsed = datetime.strptime(time_slot, "%H:%M")
    return parsed.strftime("%H:%M")


def _get_or_create_day_state(state: Dict[str, Dict[str, Dict[str, int]]], location: str, date: str) -> Dict[str, int]:
    location_state = state.setdefault(location, {})
    return location_state.setdefault(date, {})


@tool("check_restaurant_availability", description="Check available tables for a restaurant location on a date and time slot.", return_direct=False)
def check_restaurant_availability(location: str, date: str, time_slot: str) -> str:
    """Return the number of available tables at a given branch and time slot."""
    location_name = _normalize_location(location)
    if location_name not in LOCATIONS:
        return f"Sorry, {location_name} is not one of our supported locations: {', '.join(LOCATIONS)}."

    try:
        _validate_slot(time_slot)
    except ValueError as exc:
        return f"Invalid time slot: {exc}"

    state = _load_state()
    day_state = _get_or_create_day_state(state, location_name, date)
    reserved = day_state.get(time_slot, 0)
    available = TOTAL_TABLES - reserved
    return f"{location_name} has {available} of {TOTAL_TABLES} tables available on {date} at {time_slot}."


@tool("book_restaurant_table", description="Reserve a table at a restaurant location for a specific date and time slot.", return_direct=False)
def book_restaurant_table(location: str, party_size: int, date: str, time_slot: str, customer_name: str) -> str:
    """Reserve a table if capacity is still available."""
    location_name = _normalize_location(location)
    if location_name not in LOCATIONS:
        return f"Sorry, {location_name} is not one of our supported locations: {', '.join(LOCATIONS)}."

    try:
        _validate_slot(time_slot)
    except ValueError as exc:
        return f"Invalid time slot: {exc}"

    if party_size <= 0:
        return "Party size must be greater than zero."

    state = _load_state()
    day_state = _get_or_create_day_state(state, location_name, date)
    reserved = day_state.get(time_slot, 0)
    available = TOTAL_TABLES - reserved

    if available <= 0:
        return f"Sorry, {location_name} is fully booked for {date} at {time_slot}."

    if party_size > available:
        return f"Sorry, there are not enough tables available for a party of {party_size} at {location_name} on {date} at {time_slot}."

    day_state[time_slot] = reserved + 1
    _save_state(state)

    return (
        f"Reservation confirmed for {customer_name} at {location_name} on {date} at {time_slot}. "
        f"{available - 1} table(s) remain available."
    )


__all__ = [
    "LOCATIONS",
    "TOTAL_TABLES",
    "check_restaurant_availability",
    "book_restaurant_table",
    "_reset_state_for_tests",
]
