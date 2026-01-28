import json
from datetime import datetime
import pytz
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize MCP server
server = Server("business-tools-mcp-server")

# Sample inventory database
INVENTORY = {
    "laptop-dell-5000": {"name": "Dell Laptop 5000", "stock": 45, "reorder_level": 20},
    "laptop-hp-elite": {"name": "HP EliteBook", "stock": 12, "reorder_level": 15},
    "monitor-lg-27": {"name": "LG 27\" Monitor", "stock": 8, "reorder_level": 10},
    "keyboard-logitech": {"name": "Logitech Keyboard", "stock": 67, "reorder_level": 25},
    "mouse-logitech": {"name": "Logitech Mouse", "stock": 52, "reorder_level": 30}
}

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="check_inventory",
            description="Check current inventory levels for a product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product identifier (e.g., 'laptop-dell-5000')"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="get_restock_recommendations",
            description="Get recommendations for products that need restocking",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_time_in_timezone",
            description="Get current time in a specific timezone",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone name (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')"
                    }
                },
                "required": ["timezone"]
            }
        ),
        Tool(
            name="get_office_hours",
            description="Get office hours and contact info for different offices",
            inputSchema={
                "type": "object",
                "properties": {
                    "office": {
                        "type": "string",
                        "description": "Office location",
                        "enum": ["seattle", "london", "tokyo", "sydney"]
                    }
                },
                "required": ["office"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "check_inventory":
        product_id = arguments.get("product_id", "").lower()
        
        if product_id in INVENTORY:
            item = INVENTORY[product_id]
            needs_reorder = item["stock"] <= item["reorder_level"]
            
            result = {
                "product_id": product_id,
                "name": item["name"],
                "current_stock": item["stock"],
                "reorder_level": item["reorder_level"],
                "needs_reorder": needs_reorder,
                "status": "LOW STOCK" if needs_reorder else "ADEQUATE"
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        else:
            return [TextContent(type="text", text=json.dumps({"error": "Product not found"}))]
    
    elif name == "get_restock_recommendations":
        recommendations = []
        
        for product_id, item in INVENTORY.items():
            if item["stock"] <= item["reorder_level"]:
                recommendations.append({
                    "product_id": product_id,
                    "name": item["name"],
                    "current_stock": item["stock"],
                    "reorder_level": item["reorder_level"],
                    "suggested_order": item["reorder_level"] * 2 - item["stock"]
                })
        
        if recommendations:
            result = {
                "total_products_to_reorder": len(recommendations),
                "recommendations": recommendations
            }
        else:
            result = {"message": "All products adequately stocked"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_time_in_timezone":
        timezone = arguments.get("timezone")
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            result = {
                "timezone": timezone,
                "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "is_business_hours": 9 <= current_time.hour < 17,
                "day_of_week": current_time.strftime("%A")
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "get_office_hours":
        office = arguments.get("office", "").lower()
        
        office_info = {
            "seattle": {
                "timezone": "America/Los_Angeles",
                "hours": "8:00 AM - 5:00 PM PST",
                "phone": "+1-206-555-0100",
                "email": "support.seattle@contoso.com",
                "address": "123 Tech Ave, Seattle, WA 98101"
            },
            "london": {
                "timezone": "Europe/London",
                "hours": "9:00 AM - 6:00 PM GMT",
                "phone": "+44-20-5555-0100",
                "email": "support.london@contoso.com",
                "address": "45 Tech Street, London, UK EC1A 1BB"
            },
            "tokyo": {
                "timezone": "Asia/Tokyo",
                "hours": "9:00 AM - 6:00 PM JST",
                "phone": "+81-3-5555-0100",
                "email": "support.tokyo@contoso.com",
                "address": "7-8-9 Shibuya, Tokyo, Japan 150-0002"
            },
            "sydney": {
                "timezone": "Australia/Sydney",
                "hours": "8:00 AM - 5:00 PM AEDT",
                "phone": "+61-2-5555-0100",
                "email": "support.sydney@contoso.com",
                "address": "100 Harbour St, Sydney, NSW 2000"
            }
        }
        
        if office in office_info:
            return [TextContent(type="text", text=json.dumps(office_info[office], indent=2))]
        else:
            return [TextContent(type="text", text=json.dumps({"error": "Office not found"}))]
    
    return [TextContent(type="text", text=json.dumps({"error": "Tool not found"}))]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
