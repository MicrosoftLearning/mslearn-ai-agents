"""
Task 4 (Optional) - Classify and route a support ticket with the Microsoft Agent Framework.

A single triage agent reads each Tailwind Traders customer ticket and returns a structured
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
Classify the customer's support message into exactly ONE category from the list below. Provide a confidence score from 0 to 1.

Billing
- Charges, refunds, duplicate payments
- Missing or incorrect refunds on an order
- Being charged the wrong price for an order or a gear rental

Gear
- Faulty, damaged, or defective equipment
- Product setup, pairing, or usage problems
- Unexpected behavior from gear or gadgets

General
- How-to questions
- Product, trip, or stock availability
- Order history, receipts, returns, or website navigation

Important rules
- Questions about viewing, downloading, or exporting orders or receipts are General, not Billing
- Billing ONLY applies when money was charged, refunded, or paid incorrectly

Respond with ONLY a JSON object (no markdown, no extra text) using exactly these keys:
{"customer_issue": "<the customer's message>", "category": "<Billing|Gear|General>", "confidence": <number between 0 and 1>}
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
        return f"[needs detail] Low confidence ({confidence:.2f}). Ask the customer for more information."
    if category == "Billing":
        return "[escalated] Billing issue routed to the Tailwind Traders orders team."
    if category == "Gear":
        return "[auto] Gear issue: send troubleshooting steps and a return option."
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
