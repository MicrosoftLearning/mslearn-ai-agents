import json
from datetime import datetime
import pytz
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize MCP server
server = Server("it-support-mcp-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
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
    
    if name == "get_time_in_timezone":
        timezone = arguments.get("timezone")
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            result = {
                "timezone": timezone,
                "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "is_business_hours": 9 <= current_time.hour < 17
            }
            return [TextContent(type="text", text=json.dumps(result))]
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "get_office_hours":
        office = arguments.get("office", "").lower()
        
        office_info = {
            "seattle": {
                "timezone": "America/Los_Angeles",
                "hours": "8:00 AM - 5:00 PM PST",
                "phone": "+1-206-555-0100",
                "email": "support.seattle@contoso.com"
            },
            "london": {
                "timezone": "Europe/London",
                "hours": "9:00 AM - 6:00 PM GMT",
                "phone": "+44-20-5555-0100",
                "email": "support.london@contoso.com"
            },
            "tokyo": {
                "timezone": "Asia/Tokyo",
                "hours": "9:00 AM - 6:00 PM JST",
                "phone": "+81-3-5555-0100",
                "email": "support.tokyo@contoso.com"
            },
            "sydney": {
                "timezone": "Australia/Sydney",
                "hours": "8:00 AM - 5:00 PM AEDT",
                "phone": "+61-2-5555-0100",
                "email": "support.sydney@contoso.com"
            }
        }
        
        if office in office_info:
            return [TextContent(type="text", text=json.dumps(office_info[office]))]
        else:
            return [TextContent(type="text", text=json.dumps({"error": "Office not found"}))]
    
    return [TextContent(type="text", text=json.dumps({"error": "Tool not found"}))]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
