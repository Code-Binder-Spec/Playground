from mcp.client.stdio import stdio_client
from mcp import ClientSession,StdioServerParameters
import asyncio
from dotenv import load_dotenv
import os
import json
from groq import Groq

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calling_ai(client,prompt):
        messgae = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages = [
                        {"role":"user","content":f"{prompt}"}
                ]
        )
        return messgae.choices[0].message.content

def making_into_groq_format(mcp_tools):
        groq_tools = []
        for tool in mcp_tools:
                groq_tools.append(
                        {
                                "type":"function",
                                "function": {
                                        "name":tool.name,
                                        "description":tool.description,
                                        "parameters":tool.inputSchema
                                }
                        }
                )
        return groq_tools

async def main():
        server_parameters = StdioServerParameters(
                command="python",
                args=["agentic-things/mcp_testing/task3_tools.py"]
        )
        async with stdio_client(server_parameters) as (read,write):
                async with ClientSession(read,write) as session:
                         await session.initialize()
                         tool_response = await session.list_tools()
                         groq_tools = making_into_groq_format(tool_response.tools)
                         first = True
                         messages = []
                         while True:
                                   data = None
                                   if first :
                                             data = "Enter the operation of a file : "
                                             first = False
                                   user_data = str(input(data))
                                   messages.append({"role":"user","content":f"{user_data}"})
                                   response = groq_client.chat.completions.create(
                                            model="llama-3.3-70b-versatile",
                                            max_tokens=1024,
                                            messages=messages,
                                            tools=groq_tools,
                                            tool_choice="auto"
                                   )
                                   message = response.choices[0].message
                                   messages.append(message)
                                   if message.tool_calls:
                                           tool_call = message.tool_calls[0]
                                           result = await session.call_tool(tool_call.function.name,json.loads(tool_call.function.arguments))
                                           print(result)
                                           break
                                   else :
                                           data = message.content
                                           continue
asyncio.run(main())