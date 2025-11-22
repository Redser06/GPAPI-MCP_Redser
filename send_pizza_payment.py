import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    python_exe = sys.executable
    print(f"Connecting to MCP server using {python_exe}...")
    
    server_params = StdioServerParameters(
        command=python_exe,
        args=["-m", "src.main"],
        env=os.environ
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Calling send_payment_link...")
            try:
                result = await session.call_tool("send_payment_link", {
                    "params": {
                        "amount": 15.99,
                        "currency": "USD",
                        "description": "2 pizzas with pepperoni and a coke",
                        "reference": "PIZZA-ORDER-001"
                    }
                })
                print("Result:", result)
            except Exception as e:
                print(f"Error calling tool: {e}")

if __name__ == "__main__":
    asyncio.run(main())
