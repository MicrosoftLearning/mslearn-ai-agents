# Add references
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="Inventory")

# Add an inventory check mcp tool
@mcp.tool()
def get_inventory_levels() -> dict:
    """Returns current inventory for all materials."""
    return {
        "CAL-204 API": 6,
        "Excipient Blend": 8,
        "Blister Film": 28,
        "Vial Stoppers": 5,
        "Filter Cartridges": 12,
        "Sterile Vials": 9,
        "Carton Board": 30,
        "Label Stock": 3,
        "Foil Laminate": 17,
        "Desiccant Packs": 45
    }

# Add a weekly consumption mcp tool
@mcp.tool()
def get_weekly_consumption() -> dict:
    """Returns units of each material consumed last week."""
    return {
        "CAL-204 API": 22,
        "Excipient Blend": 18,
        "Blister Film": 3,
        "Vial Stoppers": 2,
        "Filter Cartridges": 14,
        "Sterile Vials": 19,
        "Carton Board": 4,
        "Label Stock": 1,
        "Foil Laminate": 13,
        "Desiccant Packs": 17
    }

# Run the MCP server
if __name__ == "__main__":
    mcp.run(show_banner=False)
