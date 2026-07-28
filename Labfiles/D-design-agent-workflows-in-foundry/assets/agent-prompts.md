# Workflow assets — copy/paste reference

These are the exact values used by the **Tailwind Traders Support Triage** workflow you
build in the portal (Tasks D1–D3). They're collected here so you can copy them straight
into the workflow visualizer instead of retyping. The instruction pages tell you *where*
each value goes.

---

## Sample support tickets (Set variable node — `Local.SupportTickets`)

Also available as [`sample_tickets.json`](./sample_tickets.json).

```json
[
    "The GPS on my TrailMate hiking watch keeps losing signal even after I did a full factory reset.",
    "Is there a way to see all of my past orders and download them as receipts?",
    "I was charged twice for the same tent order last Friday and my card statement shows two payments. Can someone fix this?"
]
```

The three tickets deliberately cover one of each category: **Gear** (watch losing signal),
**General** (viewing/downloading orders), and **Billing** (a duplicate charge).

---

## Triage agent — JSON Schema response format

```json
{
"name": "category_response",
"schema": {
    "type": "object",
    "properties": {
        "customer_issue": {
            "type": "string"
        },
        "category": {
            "type": "string"
        },
        "confidence": {
            "type": "number"
        }
    },
    "additionalProperties": false,
    "required": [
        "customer_issue",
        "category",
        "confidence"
    ]
},
"strict": true
}
```

## Triage agent — Instructions

```output
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
```

---

## Low-confidence message (Deliver a message node — Task D2)

```output
The support ticket classification has low confidence. Requesting more details about the issue: "{Local.CurrentTicket}"
```

## Confidence condition (If/Else node — Task D2)

```output
Local.TriageOutputJson.confidence > 0.6
```

---

## Category routing condition (If/Else node — Task D1)

```output
Local.TriageOutputJson.category = "Billing"
```

## Billing escalation message (Deliver a message node — Task D1)

```output
Escalate billing issue to the Tailwind Traders orders team.
```

---

## Resolution agent — Instructions (Task D3)

```output
You are a customer support resolution assistant for Tailwind Traders, an outdoor-gear retailer that also runs guided trips.

Your task is to draft a clear, professional, and friendly support response based on the issue category and customer message.

Guidelines:
If the issue category is Gear:
Suggest 1-2 common troubleshooting steps at a high level.

Avoid asking for serial numbers, order numbers, or sensitive data.

Do not imply fault by the customer.
If the issue category is General:
Provide a concise, helpful explanation or guidance.
Keep the response under 5 sentences.

Tone:
Professional, calm, and supportive
Clear and concise
No emojis

Output:
Return only the drafted response text.
Do not include internal reasoning or analysis.
```
