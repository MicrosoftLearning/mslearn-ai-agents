import json
from datetime import datetime

def _load_slots(file_path: str = "data/slots.txt") -> list:
    slots = []
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 4:
                month, day = map(int, parts[2].split("-"))
                slots.append((
                    parts[0],                          # name
                    parts[1],                          # type
                    month * 100 + day,                 # sortable month-day int
                    parts[2],                          # month-day string
                    set(parts[3].split(";")),          # sites as a set
                ))
    slots.sort(key=lambda s: s[2])
    return slots


def _load_rates(file_path: str) -> dict:
    rates = {}
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                rates[parts[0]] = float(parts[1])
    return rates

SLOTS = _load_slots()
CMO_RATES = _load_rates("data/cmo_rates.txt")
PRIORITY_MULTIPLIERS = _load_rates("data/priority_multipliers.txt")


# Determine the next open production slot at a given site
def next_available_slot(site: str) -> str:
    """Finds the next open production slot at a given site."""
    loc = site.lower()
    today = datetime.now()
    today_key = today.month * 100 + today.day

    matching = [s for s in SLOTS if loc in s[4]]
    if not matching:
        sites = sorted({x for s in SLOTS for x in s[4]})
        return json.dumps({"error": f"Unknown site '{site}'. Choose from: {', '.join(sites)}"})

    # Slots are sorted by date; pick the next one on or after today, wrapping around the year
    upcoming = next((s for s in matching if s[2] >= today_key), matching[0])

    return json.dumps({
        "slot": upcoming[0],
        "type": upcoming[1],
        "date": upcoming[3],
        "site": loc,
    })


# Calculate the cost of a tech transfer based on the tier, weeks, and priority
def calculate_transfer_cost(cmo_tier: str, weeks: float, priority: str) -> str:
    """Calculates the cost of transferring production to a contract manufacturer."""
    tier = cmo_tier.lower()
    pri = priority.lower()

    if tier not in CMO_RATES:
        return json.dumps({"error": f"Unknown CMO tier '{cmo_tier}'. Choose from: {', '.join(CMO_RATES)}"})

    if pri not in PRIORITY_MULTIPLIERS:
        return json.dumps({"error": f"Unknown priority '{priority}'. Choose from: {', '.join(PRIORITY_MULTIPLIERS)}"})

    if weeks <= 0:
        return json.dumps({"error": "Weeks must be greater than zero."})

    base_cost = CMO_RATES[tier] * weeks
    multiplier = PRIORITY_MULTIPLIERS[pri]
    total_cost = base_cost * multiplier

    return json.dumps({
        "cmo_tier": tier,
        "weeks": weeks,
        "weekly_rate": CMO_RATES[tier],
        "priority": pri,
        "priority_multiplier": multiplier,
        "base_cost": base_cost,
        "total_cost": total_cost
    })

# Draft a capacity request summarizing a production slot and a tech transfer estimate
def generate_capacity_report(slot_name: str, site: str, cmo_tier: str, weeks: float, priority: str, requested_by: str) -> str:
    """
    Drafts a capacity request for review and saves it to a file.

    Returns:
        JSON string with the file path of the generated draft.
    """
    cost_result = json.loads(calculate_transfer_cost(cmo_tier, weeks, priority))
    slot_result = json.loads(next_available_slot(site))

    if "error" in cost_result:
        return json.dumps(cost_result)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"request_{slot_name.replace(' ', '_').lower()}_{timestamp.replace(':', '').replace(' ', '_')}.txt"

    report = f"""======================================
  CALDOVA - CAPACITY REQUEST (DRAFT)
======================================
Date:           {timestamp}
Requested by:   {requested_by}
Slot:           {slot_name}
Site:           {site}

NEXT OPEN SLOT
  Slot:         {slot_result.get('slot', 'N/A')}
  Date:         {slot_result.get('date', 'N/A')}

CONTRACT MANUFACTURER
  Tier:         {cost_result['cmo_tier']}
  Weeks:        {cost_result['weeks']}
  Weekly Rate:  ${cost_result['weekly_rate']:.2f}K
  Priority:     {cost_result['priority']}
  Multiplier:   {cost_result['priority_multiplier']}x

COST SUMMARY
  Base Cost:    ${cost_result['base_cost']:.2f}K
  Total Cost:   ${cost_result['total_cost']:.2f}K

This is a draft for planning review. It does not reserve capacity or commit spend.
======================================
"""

    with open(filename, "w") as f:
        f.write(report)

    return json.dumps({"status": "Draft capacity request generated", "file": filename})
