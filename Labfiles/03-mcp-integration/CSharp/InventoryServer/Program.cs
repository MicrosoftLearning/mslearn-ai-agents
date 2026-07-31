// Custom MCP server -- C# port of server.py. Hosts the same two tools (inventory levels, weekly
// sales) over stdio, using the official ModelContextProtocol SDK instead of Python's FastMCP.
// Run standalone to test manually, or let InventoryClient spawn it automatically.

using InventoryServer;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddMcpServer()
    .WithStdioServerTransport()
    .WithTools<InventoryTools>();

// stdout is reserved for the MCP protocol -- route logs to stderr, same reason server.py
// passes show_banner=False to mcp.run().
builder.Logging.AddConsole(options => options.LogToStandardErrorThreshold = LogLevel.Trace);

await builder.Build().RunAsync();
