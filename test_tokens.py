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
            
            print("\n--- Testing List Tokens ---")
            try:
                result = await session.call_tool("list_tokens", {
                    "params": {
                        "page": 1,
                        "page_size": 5
                    }
                })
                print("List Tokens Result:", result)
            except Exception as e:
                print(f"Error listing tokens: {e}")

            print("\n--- Testing Create Token ---")
            try:
                result = await session.call_tool("create_token", {
                    "params": {
                        "payment_method": {
                            "card_number": "4622943123052970",
                            "expiry_month": "10",
                            "expiry_year": "2027",
                            "cvn": "123"
                        },
                        "usage_mode": "MULTIPLE",
                        "description": "User Test Token"
                    }
                })
                print("Create Token Result:", result)
            except Exception as e:
                print(f"Error creating token: {e}")

            print("\n--- Testing Risk Assessment ---")
            try:
                result = await session.call_tool("assess_risk", {
                    "params": {
                        "amount": 100.00,
                        "currency": "USD",
                        "payment_method": {
                            "card_number": "4111111111111111",
                            "expiry_month": "12",
                            "expiry_year": "2025",
                            "cvn": "123"
                        }
                    }
                })
                print("Risk Assessment Result:", result)
            except Exception as e:
                print(f"Error assessing risk: {e}")

if __name__ == "__main__":
    asyncio.run(main())
