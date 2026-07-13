import json
from datetime import datetime

def _load_trips(file_path: str = "data/trips.txt") -> list:
    trips = []
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 4:
                month, day = map(int, parts[2].split("-"))
                trips.append((
                    parts[0],                          # name
                    parts[1],                          # type
                    month * 100 + day,                 # sortable month-day int
                    parts[2],                          # month-day string
                    set(parts[3].split(";")),          # regions as a set
                ))
    trips.sort(key=lambda t: t[2])
    return trips


def _load_rates(file_path: str) -> dict:
    rates = {}
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                rates[parts[0]] = float(parts[1])
    return rates

TRIPS = _load_trips()
RENTAL_RATES = _load_rates("data/rental_rates.txt")
SERVICE_MULTIPLIERS = _load_rates("data/service_multipliers.txt")


# Determine the next available guided trip for a given region
def next_available_trip(region: str) -> str:
    """Finds the next guided trip departing in a given region."""
    reg = region.lower()
    today = datetime.now()
    today_key = today.month * 100 + today.day

    matching = [t for t in TRIPS if reg in t[4]]
    if not matching:
        regions = sorted({r for t in TRIPS for r in t[4]})
        return json.dumps({"error": f"Unknown region '{region}'. Choose from: {', '.join(regions)}"})

    # Trips are sorted by date; pick the next one on or after today, wrapping around the year
    upcoming = next((t for t in matching if t[2] >= today_key), matching[0])

    return json.dumps({
        "trip": upcoming[0],
        "type": upcoming[1],
        "date": upcoming[3],
        "region": reg,
    })


# Calculate the cost of a gear rental based on the tier, days, and service level
def calculate_rental_cost(gear_tier: str, days: float, service_level: str) -> str:
    """Calculates the cost of a gear rental."""
    tier = gear_tier.lower()
    svc = service_level.lower()

    if tier not in RENTAL_RATES:
        return json.dumps({"error": f"Unknown gear tier '{gear_tier}'. Choose from: {', '.join(RENTAL_RATES)}"})

    if svc not in SERVICE_MULTIPLIERS:
        return json.dumps({"error": f"Unknown service level '{service_level}'. Choose from: {', '.join(SERVICE_MULTIPLIERS)}"})

    if days <= 0:
        return json.dumps({"error": "Days must be greater than zero."})

    base_cost = RENTAL_RATES[tier] * days
    multiplier = SERVICE_MULTIPLIERS[svc]
    total_cost = base_cost * multiplier

    return json.dumps({
        "gear_tier": tier,
        "days": days,
        "daily_rate": RENTAL_RATES[tier],
        "service_level": svc,
        "service_multiplier": multiplier,
        "base_cost": base_cost,
        "total_cost": total_cost
    })

# Generate a booking report summarizing the details of a guided trip and gear rental
def generate_booking_report(trip_name: str, region: str, gear_tier: str, days: float, service_level: str, customer_name: str) -> str:
    """
    Generates a trip booking report and saves it to a file.

    Returns:
        JSON string with the file path of the generated report.
    """
    cost_result = json.loads(calculate_rental_cost(gear_tier, days, service_level))
    trip_result = json.loads(next_available_trip(region))

    if "error" in cost_result:
        return json.dumps(cost_result)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"report_{trip_name.replace(' ', '_').lower()}_{timestamp.replace(':', '').replace(' ', '_')}.txt"

    report = f"""======================================
  CONTOSO ADVENTURE WORKS - BOOKING REPORT
======================================
Date:           {timestamp}
Customer:       {customer_name}
Trip:           {trip_name}
Region:         {region}

NEXT AVAILABLE TRIP
  Trip:         {trip_result.get('trip', 'N/A')}
  Date:         {trip_result.get('date', 'N/A')}

GEAR RENTAL
  Tier:         {cost_result['gear_tier']}
  Days:         {cost_result['days']}
  Daily Rate:   ${cost_result['daily_rate']:.2f}
  Service:      {cost_result['service_level']}
  Multiplier:   {cost_result['service_multiplier']}x

COST SUMMARY
  Base Cost:    ${cost_result['base_cost']:.2f}
  Total Cost:   ${cost_result['total_cost']:.2f}
======================================
"""

    with open(filename, "w") as f:
        f.write(report)

    return json.dumps({"status": "Report generated", "file": filename})
