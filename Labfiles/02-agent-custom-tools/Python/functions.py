import json
from datetime import datetime

def _load_events(file_path: str = "data/events.txt") -> list:
    events = []
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 4:
                month, day = map(int, parts[2].split("-"))
                events.append((
                    parts[0],                          # name
                    parts[1],                          # type
                    month * 100 + day,                 # sortable month-day int
                    parts[2],                          # month-day string
                    set(parts[3].split(";")),          # locations as a set
                ))
    events.sort(key=lambda e: e[2])
    return events


def _load_rates(file_path: str) -> dict:
    rates = {}
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                rates[parts[0]] = float(parts[1])
    return rates

EVENTS = _load_events()
TELESCOPE_RATES = _load_rates("data/telescope_rates.txt")
PRIORITY_MULTIPLIERS = _load_rates("data/priority_multipliers.txt")

# Determine the next visible astronomical event for a given location


# Calculate the cost of telescope observation time based on the tier, hours, and priority
def calculate_observation_cost(telescope_tier: str, hours: float, priority: str) -> str:
    """Calculates the cost of telescope observation time."""
    tier = telescope_tier.lower()
    pri = priority.lower()

    if tier not in TELESCOPE_RATES:
        return json.dumps({"error": f"Unknown telescope tier '{telescope_tier}'. Choose from: {', '.join(TELESCOPE_RATES)}"})

    if pri not in PRIORITY_MULTIPLIERS:
        return json.dumps({"error": f"Unknown priority '{priority}'. Choose from: {', '.join(PRIORITY_MULTIPLIERS)}"})

    if hours <= 0:
        return json.dumps({"error": "Hours must be greater than zero."})

    base_cost = TELESCOPE_RATES[tier] * hours
    multiplier = PRIORITY_MULTIPLIERS[pri]
    total_cost = base_cost * multiplier

    return json.dumps({
        "telescope_tier": tier,
        "hours": hours,
        "hourly_rate": TELESCOPE_RATES[tier],
        "priority": pri,
        "priority_multiplier": multiplier,
        "base_cost": base_cost,
        "total_cost": total_cost
    })

# Generate an observation report summarizing the details of an astronomical observation session
def generate_observation_report(event_name: str, location: str, telescope_tier: str, hours: float, priority: str, observer_name: str) -> str:
    """
    Generates an observation session report and saves it to a file.

    Returns:
        JSON string with the file path of the generated report.
    """
    cost_result = json.loads(calculate_observation_cost(telescope_tier, hours, priority))
    event_result = json.loads(next_visible_event(location))

    if "error" in cost_result:
        return json.dumps(cost_result)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"report_{event_name.replace(' ', '_').lower()}_{timestamp.replace(':', '').replace(' ', '_')}.txt"

    report = f"""======================================
  CONTOSO OBSERVATORIES - SESSION REPORT
======================================
Date:           {timestamp}
Observer:       {observer_name}
Event:          {event_name}
Location:       {location}

NEXT VISIBLE EVENT
  Event:        {event_result.get('event', 'N/A')}
  Date:         {event_result.get('date', 'N/A')}

TELESCOPE BOOKING
  Tier:         {cost_result['telescope_tier']}
  Hours:        {cost_result['hours']}
  Hourly Rate:  ${cost_result['hourly_rate']:.2f}
  Priority:     {cost_result['priority']}
  Multiplier:   {cost_result['priority_multiplier']}x

COST SUMMARY
  Base Cost:    ${cost_result['base_cost']:.2f}
  Total Cost:   ${cost_result['total_cost']:.2f}
======================================
"""

    with open(filename, "w") as f:
        f.write(report)

    return json.dumps({"status": "Report generated", "file": filename})