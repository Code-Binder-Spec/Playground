from mcp.client.stdio import stdio_client
from mcp import ClientSession,StdioServerParameters
import asyncio
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from groq import Groq

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calling_ai(client,prompt):
        messgae = client.chat.completions.create(
                model="openai/gpt-oss-120b",
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
                                        "parameters":tool.input_schema
                                }
                        }
                )
        return groq_tools


async def actual_agentic_function(messages,groq_tools,session):
        data = None
        while True:
                            response = groq_client.chat.completions.create(
                                                             model="openai/gpt-oss-120b",
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
                                        print(tool_call.function.name)
                                        print(tool_call.function.arguments)
                                        print(result.content[0].text)
                                        messages.append(
                                                                         {
                                                                             "role":"tool",
                                                                             "tool_call_id":tool_call.id,
                                                                             "content":result.content[0].text
                                                                                              }
                                                                                   )
                                        ai_reply = calling_ai(groq_client,f"You are evaluating whether an AI agent correctly fulfilled a user's request by calling the appropriate tool(s). You will be given the full conversation history, including the user's request, which tools the agent called, with what arguments, and the results returned. Your only job is to judge whether the agent's tool calls functionally satisfied what the user actually asked for. The number of tool calls, which specific tools were used, or the order of calls does not matter — only whether the end result accomplishes what the user needed. If the agent's actions correctly satisfied the user's request, respond with exactly: CORRECT. If the agent's actions did NOT satisfy the user's request, respond with: DIDNT APPROVED, followed by a brief, specific reason why.\n\nConversational history : {messages}")
                                        print(ai_reply)
                                        if "correct" in ai_reply.lower():
                                                                        data = ("correct",result.content[0].text)
                                                                        break
                                        else :
                                                                        messages.append({"role":"system","content":f"{ai_reply}"})
                                                                        continue
                            else :
                                    data = ("again",response.choices[0].message.content)
                                    break
        return data
                
        
async def main():
        server_parameters = StdioServerParameters(
                command="python",
                args=["/home/coder/coding/Playground/agentic-things/mcp_testing/task3_tools.py"]
        )
        async with stdio_client(server_parameters) as (read,write):
                async with ClientSession(read,write) as session:
                         await session.initialize()
                         tool_response = await session.list_tools()
                         groq_tools = making_into_groq_format(tool_response.tools)
                         object_home = Path.home()
                         string_home = str(object_home)
                         first = True
                         messages = [
                                  {"role": "system", "content": f"Whenever a task requires a file or folder, follow these rules. If the user refers to their home directory by itself (with no further location specified), use exactly this path: {string_home} . If the user's request goes beyond just the home directory — naming a specific file or folder inside it — call finding_real_path_of_entry with just that name (not a full path). Otherwise, for any task requiring a file or folder, always call finding_real_path_of_entry first with just the name before calling any other tool. If it returns a single path, use that exact path for the next tool call. If it returns multiple matches, do not proceed — list the matches for the user and ask which one they mean, then use their answer to select the correct path before calling the next tool. If it returns that the path doesn't exist, tell the user and do not proceed with any further tool call."}
                         ]
                         data = None
                         first_prompt = "Enter the operation of a file "
     
                         while True:
                                               if first :
                                                          data = first_prompt
                                                          first = False
                                               user_data = str(input(data+" : "))
                                               messages.append({"role":"user","content":f"{user_data}"})
                                               result = await actual_agentic_function(messages,groq_tools,session)
                                               if "correct" in result:
                                                       
                                                       print(f"{result[1]} : task completed")
                                                       break
                                               else :
                                                       data = result[1]
                                                       continue
asyncio.run(main())