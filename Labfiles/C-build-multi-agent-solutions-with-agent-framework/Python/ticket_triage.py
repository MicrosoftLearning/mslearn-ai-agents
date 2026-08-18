"""
Task 4 (Optional) - Classify and route a support ticket with the Microsoft Agent Framework.

A single triage agent reads each Caldova support ticket and returns a structured
classification (category + confidence). Your code then routes the ticket: low-confidence
tickets go back for more detail, billing issues are escalated, and everything else is handled
automatically. This shows how one agent's structured output can drive conditional routing in
code - the same classify-then-branch pattern you would otherwise build into a larger workflow.

Follow the task instructions to add code at each commented placeholder.
"""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Add references


load_dotenv()

# Tickets below this confidence are sent back for more detail instead of routed.
CONFIDENCE_THRESHOLD = 0.6

# The triage agent must return a strict JSON classification so code can route on it.
TRIAGE_INSTRUCTIONS = """
Classify the support message into exactly ONE category from the list below. Provide a confidence score from 0 to 1.

Billing
- Charges, credits, duplicate payments
- Missing or incorrect credits on an invoice
- Being invoiced the wrong amount for a transfer week

Equipment
- Faulty, damaged, or defective equipment
- Equipment setup, calibration, or usage problems
- Unexpected behavior from equipment or systems

General
- How-to questions
- Material, slot, or stock availability
- Request history, reports, or portal navigation

Important rules
- Questions about viewing, downloading, or exporting requests or reports are General, not Billing
- Billing ONLY applies when money was invoiced, credited, or paid incorrectly

Respond with ONLY a JSON object (no markdown, no extra text) using exactly these keys:
{"reported_issue": "<the reported message>", "category": "<Billing|Equipment|General>", "confidence": <number between 0 and 1>}
"""


def parse_classification(text):
    """Pull the JSON classification out of the agent's reply."""
    cleaned = text.strip()
    # The model sometimes wraps JSON in a ```json ... ``` fence; strip it if present.
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1:
        cleaned = cleaned[start:end + 1]
    return json.loads(cleaned)


def route_ticket(classification):
    """Decide what happens to a ticket based on its category and confidence."""
    category = (classification.get("category") or "").strip()
    confidence = float(classification.get("confidence", 0))

    if confidence < CONFIDENCE_THRESHOLD:
        return f"[needs detail] Low confidence ({confidence:.2f}). Ask the requester for more information."
    if category == "Billing":
        return "[escalated] Billing issue routed to the Caldova procurement team."
    if category == "Equipment":
        return "[auto] Equipment issue: send troubleshooting steps and raise a maintenance job."
    if category == "General":
        return "[auto] General question: reply with a help-center answer."
    return f"[review] Unrecognized category '{category}'. Send for manual review."


async def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Load the sample tickets
    script_dir = Path(__file__).parent
    tickets = json.loads((script_dir / "sample_tickets.json").read_text())

    # Create a foundry chat client


    # Create the triage agent


    # Classify and route each ticket
    for number, ticket in enumerate(tickets, start=1):
        print(f"\nTicket {number}: {ticket}")

        # Create a session, classify the ticket, then parse and route the result
        pass


if __name__ == "__main__":
    asyncio.run(main())
