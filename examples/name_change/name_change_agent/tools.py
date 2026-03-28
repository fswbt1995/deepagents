"""Name Change Tools.

This module provides verification and processing utilities for the name change agent,
using mock data for passenger details, flight information, and airline policies.
"""

import random
from datetime import datetime, timedelta
from langchain_core.tools import tool
from typing_extensions import Annotated, Literal


# Mock data for demonstration
MOCK_PASSENGERS = {
    "ABC123": {
        "name": "John Smith",
        "flight": "AA101",
        "departure": "2026-03-30 08:00",
        "status": "confirmed"
    },
    "XYZ789": {
        "name": "Jane Doe",
        "flight": "UA202",
        "departure": "2026-03-31 14:30",
        "status": "confirmed"
    },
    "DEF456": {
        "name": "Bob Johnson",
        "flight": "DL303",
        "departure": "2026-03-29 10:15",
        "status": "confirmed"
    }
}

MOCK_FLIGHTS = {
    "AA101": {
        "airline": "American Airlines",
        "route": "JFK-LAX",
        "departure": "2026-03-30 08:00",
        "status": "on-time"
    },
    "UA202": {
        "airline": "United Airlines",
        "route": "ORD-SFO",
        "departure": "2026-03-31 14:30",
        "status": "on-time"
    },
    "DL303": {
        "airline": "Delta Airlines",
        "route": "ATL-MIA",
        "departure": "2026-03-29 10:15",
        "status": "delayed"
    }
}

AIRLINE_POLICIES = {
    "name_change": {
        "fee": "$75",
        "deadline": "24 hours before departure",
        "conditions": "Spelling corrections free, full name changes subject to fee",
        "restrictions": "No changes within 24 hours of departure"
    }
}


@tool(parse_docstring=True)
def passenger_lookup(
    booking_reference: str,
    passenger_name: str = None,
) -> str:
    """Look up passenger details and booking information.

    Searches the airline's booking system for passenger details using booking reference
    and optionally passenger name for verification.

    Args:
        booking_reference: The booking reference number (e.g., ABC123)
        passenger_name: Optional passenger name for additional verification

    Returns:
        Formatted passenger booking details
    """
    if booking_reference in MOCK_PASSENGERS:
        passenger = MOCK_PASSENGERS[booking_reference]
        flight_info = MOCK_FLIGHTS.get(passenger["flight"], {})

        # Simulate some verification logic
        name_match = passenger_name is None or passenger_name.lower() in passenger["name"].lower()

        result = f"""## Passenger Details Found
**Booking Reference:** {booking_reference}
**Passenger Name:** {passenger["name"]}
**Flight:** {passenger["flight"]} ({flight_info.get("route", "Unknown route")})
**Departure:** {passenger["departure"]}
**Status:** {passenger["status"]}
**Name Match:** {"✓ Verified" if name_match else "✗ Mismatch"}

---
"""
    else:
        result = f"""## Passenger Not Found
**Booking Reference:** {booking_reference}
**Status:** No booking found with this reference

---
"""

    return result


@tool(parse_docstring=True)
def flight_lookup(
    flight_number: str,
    date: str = None,
) -> str:
    """Look up flight details and schedule information.

    Retrieves current flight status, schedule, and operational details.

    Args:
        flight_number: The flight number (e.g., AA101)
        date: Optional date filter (YYYY-MM-DD format)

    Returns:
        Formatted flight details and status
    """
    if flight_number in MOCK_FLIGHTS:
        flight = MOCK_FLIGHTS[flight_number]

        # Simulate real-time status updates
        current_time = datetime.now()
        departure_time = datetime.strptime(flight["departure"], "%Y-%m-%d %H:%M")
        time_until_departure = departure_time - current_time

        if time_until_departure < timedelta(hours=24):
            status_note = "⚠️ Within 24-hour change window"
        else:
            status_note = "✓ Eligible for name changes"

        result = f"""## Flight Details Found
**Flight Number:** {flight_number}
**Airline:** {flight["airline"]}
**Route:** {flight["route"]}
**Scheduled Departure:** {flight["departure"]}
**Current Status:** {flight["status"]}
**Change Eligibility:** {status_note}

---
"""
    else:
        result = f"""## Flight Not Found
**Flight Number:** {flight_number}
**Status:** No flight found with this number

---
"""

    return result


@tool(parse_docstring=True)
def policy_check(
    policy_type: Annotated[
        Literal["name_change", "cancellation", "refund"], "default"
    ] = "name_change",
) -> str:
    """Check airline policies for various operations.

    Retrieves current airline policies and procedures for the specified operation type.

    Args:
        policy_type: Type of policy to check (name_change, cancellation, refund)

    Returns:
        Formatted policy details and requirements
    """
    if policy_type == "name_change":
        policy = AIRLINE_POLICIES["name_change"]

        result = f"""## Name Change Policy
**Fee:** {policy["fee"]}
**Deadline:** {policy["deadline"]}
**Conditions:** {policy["conditions"]}
**Restrictions:** {policy["restrictions"]}

**Processing Notes:**
- Spelling corrections are typically free
- Full name changes incur a processing fee
- Changes must be made before the deadline
- Government-issued ID required for verification

---
"""
    else:
        result = f"""## Policy Information
**Policy Type:** {policy_type}
**Status:** Policy details not available for this type

---
"""

    return result


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on name change processing progress and decision-making.

    Use this tool after each verification to analyze results and plan next steps systematically.
    This creates a deliberate pause in the processing workflow for quality decision-making.

    When to use:
    - After receiving verification results: What key information did I confirm?
    - Before deciding next steps: Do I have enough to approve/deny the change?
    - When assessing processing gaps: What specific information am I still missing?
    - Before concluding processing: Can I provide a final determination now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I verified?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence for a good decision?
    4. Strategic decision - Should I continue checking or provide my determination?

    Args:
        reflection: Your detailed reflection on processing progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"