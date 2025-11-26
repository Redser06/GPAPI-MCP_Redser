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
            
            print("\n--- Testing List Disputes ---")
            try:
                result = await session.call_tool("list_disputes", {
                    "params": {
                        "page": 1,
                        "page_size": 5
                    }
                })
                print("List Disputes Result:", result)
            except Exception as e:
                print(f"Error listing disputes: {e}")

            print("\n--- Testing List Settlements ---")
            try:
                result = await session.call_tool("list_settlements", {
                    "params": {
                        "page": 1,
                        "page_size": 5
                    }
                })
                print("List Settlements Result:", result)
            except Exception as e:
                print(f"Error listing settlements: {e}")

if __name__ == "__main__":
    asyncio.run(main())
