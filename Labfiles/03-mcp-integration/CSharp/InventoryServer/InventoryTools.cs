using System.ComponentModel;
using System.Text.Json;
using ModelContextProtocol.Server;

namespace InventoryServer;

// C# port of the tools defined in server.py. [McpServerToolType] marks this class as a
// container for tools; [McpServerTool] marks each method as one, discoverable the same way
// functions.py's functions become discoverable when decorated with @mcp.tool().
[McpServerToolType]
public sealed class InventoryTools
{
    [McpServerTool, Description("Returns current inventory for all products.")]
    public static string GetInventoryLevels() => JsonSerializer.Serialize(new Dictionary<string, int>
    {
        ["Moisturizer"] = 6,
        ["Shampoo"] = 8,
        ["Body Spray"] = 28,
        ["Hair Gel"] = 5,
        ["Lip Balm"] = 12,
        ["Skin Serum"] = 9,
        ["Cleanser"] = 30,
        ["Conditioner"] = 3,
        ["Setting Powder"] = 17,
        ["Dry Shampoo"] = 45,
    });

    [McpServerTool, Description("Returns number of units sold last week.")]
    public static string GetWeeklySales() => JsonSerializer.Serialize(new Dictionary<string, int>
    {
        ["Moisturizer"] = 22,
        ["Shampoo"] = 18,
        ["Body Spray"] = 3,
        ["Hair Gel"] = 2,
        ["Lip Balm"] = 14,
        ["Skin Serum"] = 19,
        ["Cleanser"] = 4,
        ["Conditioner"] = 1,
        ["Setting Powder"] = 13,
        ["Dry Shampoo"] = 17,
    });
}
