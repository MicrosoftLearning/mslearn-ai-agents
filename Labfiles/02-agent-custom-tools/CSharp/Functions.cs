using System.ComponentModel;
using System.Text.Json;
using System.Text.Json.Nodes;

// Local function tools for the astronomy agent. C# port of functions.py -- each method here
// maps 1:1 to a Python function of the same name. [Description] attributes are what let
// AIFunctionFactory.Create(...) generate the tool's JSON schema automatically from the method
// signature (see Program.cs), instead of hand-writing the schema like the Python sample does.
static class Functions
{
    private static readonly List<(string Name, string Type, int SortKey, string DateText, HashSet<string> Locations)> Events = LoadEvents("data/events.txt");
    private static readonly Dictionary<string, double> TelescopeRates = LoadRates("data/telescope_rates.txt");
    private static readonly Dictionary<string, double> PriorityMultipliers = LoadRates("data/priority_multipliers.txt");

    [Description("Get the next visible astronomical event for a given location.")]
    public static string NextVisibleEvent(
        [Description("Continent to find the next visible event in (e.g. 'north_america', 'south_america', 'australia')")] string location)
    {
        int today = int.Parse(DateTime.Now.ToString("MMdd"));
        string loc = location.ToLowerInvariant().Replace(" ", "_");

        foreach (var (name, type, sortKey, dateText, locations) in Events)
        {
            if (locations.Contains(loc) && sortKey >= today)
            {
                return JsonSerializer.Serialize(new JsonObject
                {
                    ["event"] = name,
                    ["type"] = type,
                    ["date"] = dateText,
                    ["visible_from"] = new JsonArray(locations.OrderBy(l => l).Select(l => (JsonNode)l).ToArray()),
                });
            }
        }

        return JsonSerializer.Serialize(new JsonObject { ["message"] = $"No upcoming events found for {location}." });
    }

    [Description("Calculate the cost of an observation based on the telescope tier, number of hours, and priority level.")]
    public static string CalculateObservationCost(
        [Description("The tier of the telescope (e.g. 'standard', 'advanced', 'premium')")] string telescopeTier,
        [Description("The number of hours for the observation")] double hours,
        [Description("The priority level of the observation (e.g. 'low', 'normal', 'high')")] string priority)
    {
        string tier = telescopeTier.ToLowerInvariant();
        string pri = priority.ToLowerInvariant();

        if (!TelescopeRates.TryGetValue(tier, out double hourlyRate))
        {
            return JsonSerializer.Serialize(new JsonObject { ["error"] = $"Unknown telescope tier '{telescopeTier}'. Choose from: {string.Join(", ", TelescopeRates.Keys)}" });
        }

        if (!PriorityMultipliers.TryGetValue(pri, out double multiplier))
        {
            return JsonSerializer.Serialize(new JsonObject { ["error"] = $"Unknown priority '{priority}'. Choose from: {string.Join(", ", PriorityMultipliers.Keys)}" });
        }

        if (hours <= 0)
        {
            return JsonSerializer.Serialize(new JsonObject { ["error"] = "Hours must be greater than zero." });
        }

        double baseCost = hourlyRate * hours;
        double totalCost = baseCost * multiplier;

        return JsonSerializer.Serialize(new JsonObject
        {
            ["telescope_tier"] = tier,
            ["hours"] = hours,
            ["hourly_rate"] = hourlyRate,
            ["priority"] = pri,
            ["priority_multiplier"] = multiplier,
            ["base_cost"] = baseCost,
            ["total_cost"] = totalCost,
        });
    }

    [Description("Generate a report summarizing an astronomical observation.")]
    public static string GenerateObservationReport(
        [Description("The name of the astronomical event being observed")] string eventName,
        [Description("The location of the observer")] string location,
        [Description("The tier of the telescope used for the observation (e.g. 'standard', 'advanced', 'premium')")] string telescopeTier,
        [Description("The number of hours the telescope was used for the observation")] double hours,
        [Description("The priority level of the observation (e.g. 'low', 'normal', 'high')")] string priority,
        [Description("The name of the person who conducted the observation")] string observerName)
    {
        JsonNode costResult = JsonNode.Parse(CalculateObservationCost(telescopeTier, hours, priority))!;
        if (costResult["error"] is not null)
        {
            return costResult.ToJsonString();
        }

        JsonNode eventResult = JsonNode.Parse(NextVisibleEvent(location))!;

        DateTime now = DateTime.Now;
        string timestamp = now.ToString("yyyy-MM-dd HH:mm");
        string filename = $"report_{eventName.Replace(' ', '_').ToLowerInvariant()}_{now:yyyy-MM-dd_HHmm}.txt";

        double hourlyRate = (double)costResult["hourly_rate"]!;
        double baseCost = (double)costResult["base_cost"]!;
        double totalCost = (double)costResult["total_cost"]!;

        string report = $"""
            ======================================
              CONTOSO OBSERVATORIES - SESSION REPORT
            ======================================
            Date:           {timestamp}
            Observer:       {observerName}
            Event:          {eventName}
            Location:       {location}

            NEXT VISIBLE EVENT
              Event:        {(string?)eventResult["event"] ?? "N/A"}
              Date:         {(string?)eventResult["date"] ?? "N/A"}

            TELESCOPE BOOKING
              Tier:         {(string?)costResult["telescope_tier"]}
              Hours:        {(double)costResult["hours"]!}
              Hourly Rate:  ${hourlyRate:F2}
              Priority:     {(string?)costResult["priority"]}
              Multiplier:   {(double)costResult["priority_multiplier"]!}x

            COST SUMMARY
              Base Cost:    ${baseCost:F2}
              Total Cost:   ${totalCost:F2}
            ======================================

            """;

        File.WriteAllText(filename, report);

        return JsonSerializer.Serialize(new JsonObject { ["status"] = "Report generated", ["file"] = filename });
    }

    private static List<(string, string, int, string, HashSet<string>)> LoadEvents(string path)
    {
        var events = new List<(string, string, int, string, HashSet<string>)>();

        foreach (string line in File.ReadAllLines(path))
        {
            string[] parts = line.Trim().Split('|');
            if (parts.Length != 4)
            {
                continue;
            }

            string[] monthDay = parts[2].Split('-');
            int sortKey = int.Parse(monthDay[0]) * 100 + int.Parse(monthDay[1]);
            var locations = parts[3].Split(';').ToHashSet();

            events.Add((parts[0], parts[1], sortKey, parts[2], locations));
        }

        return events.OrderBy(e => e.Item3).ToList();
    }

    private static Dictionary<string, double> LoadRates(string path)
    {
        var rates = new Dictionary<string, double>();

        foreach (string line in File.ReadAllLines(path))
        {
            string[] parts = line.Trim().Split('|');
            if (parts.Length == 2)
            {
                rates[parts[0]] = double.Parse(parts[1]);
            }
        }

        return rates;
    }
}
