from mcp.server import MCPServer

mcp = MCPServer("testing_first_time")

@mcp.tool()
def add_numbers(a:int,b:int) -> int:
    """Add two numbers together"""
    return a+b

if __name__ == "__main__":
    mcp.run()
