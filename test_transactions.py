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
            
            print("\n--- Testing List Transactions ---")
            try:
                result = await session.call_tool("list_transactions", {
                    "params": {
                        "page": 1,
                        "page_size": 5
                    }
                })
                print("List Transactions Result:", result)
            except Exception as e:
                print(f"Error listing transactions: {e}")

            print("\n--- Testing Create Sale ---")
            try:
                result = await session.call_tool("create_sale", {
                    "params": {
                        "amount": 10.00,
                        "currency": "USD",
                        "description": "Test Sale",
                        "reference": "TEST-SALE-001"
                    }
                })
                print("Create Sale Result:", result)
            except Exception as e:
                print(f"Error creating sale: {e}")

if __name__ == "__main__":
    asyncio.run(main())
