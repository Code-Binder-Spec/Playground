from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def main():
    server_parametres = StdioServerParameters(
        command="python",
        args=["agentic-things/mcp_testing/task1_tool.py"],
    )
    async with stdio_client(server_parametres) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            result = await session.call_tool("add_numbers",{"a":5,"b":12})
            print(result)

if __name__ == "__main__":
     asyncio.run(main())
