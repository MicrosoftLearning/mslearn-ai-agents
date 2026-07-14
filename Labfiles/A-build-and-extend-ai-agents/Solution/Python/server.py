# Add references
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="Inventory")

# Add an inventory check mcp tool
@mcp.tool()
def get_inventory_levels() -> dict:
    """Returns current inventory for all products."""
    return {
        "Tent": 6,
        "Sleeping Bag": 8,
        "Trekking Poles": 28,
        "Headlamp": 5,
        "Water Filter": 12,
        "Camp Stove": 9,
        "Backpack": 30,
        "Rain Jacket": 3,
        "Hiking Boots": 17,
        "Trail Snacks": 45
    }

# Add a weekly sales mcp tool
@mcp.tool()
def get_weekly_sales() -> dict:
    """Returns number of units sold last week."""
    return {
        "Tent": 22,
        "Sleeping Bag": 18,
        "Trekking Poles": 3,
        "Headlamp": 2,
        "Water Filter": 14,
        "Camp Stove": 19,
        "Backpack": 4,
        "Rain Jacket": 1,
        "Hiking Boots": 13,
        "Trail Snacks": 17
    }

# Run the MCP server
if __name__ == "__main__":
    mcp.run(show_banner=False)
