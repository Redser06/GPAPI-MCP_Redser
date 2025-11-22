"""Main entry point for the MCP GPAPI server."""

import sys
from mcp.server import FastMCP
from mcp.server import FastMCP
from dotenv import load_dotenv

load_dotenv()

from .tools import PaymentTools

def main():
    """Start the MCP server."""
    # Create MCP server instance
    server = FastMCP("mcp-gpapi")
    
    # Register tools
    payment_tools = PaymentTools()
    server.add_tool(payment_tools.process_payment)
    server.add_tool(payment_tools.send_payment_link)
    
    try:
        # Start server
        server.run()
    except KeyboardInterrupt:
        print("Server shutting down...", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()