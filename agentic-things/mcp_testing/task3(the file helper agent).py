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
                                                                             "Content":{result.content[0].text}
                                                                                              }
                                                                                   )
                                        ai_reply = calling_ai(groq_client,f"You are evaluating whether an AI agent correctly fulfilled a user's request by calling the appropriate tool(s). You will be given the full conversation history, including the user's request, which tools the agent called, with what arguments, and the results returned. Your only job is to judge whether the agent's tool calls functionally satisfied what the user actually asked for. The number of tool calls, which specific tools were used, or the order of calls does not matter — only whether the end result accomplishes what the user needed. If the agent's actions correctly satisfied the user's request, respond with exactly: CORRECT. If the agent's actions did NOT satisfy the user's request, respond with: INCORRECT, followed by a brief, specific reason why.\n\nConversational history : {messages}")
                                        print(ai_reply)
                                        if "correct" in ai_reply.lower():
                                                                        data = ("correct",result.content[0].text)
                                                                        break
                                        else :
                                                                        messages.append({"role":"system","Reason for failiure":f"{ai_reply}"})
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
                         first = True
                         messages = [
                                  {"role": "system", "content": "When a task requires a file or folder path, follow these rules exactly. First, the user must specify at least two location segments (for example, 'documents/testing', not just 'testing' alone) before you call any path-related tool. If the user provides only a single, bare location with no further context, do not call a tool — ask a clarifying question asking for the fuller path instead. Second, if the user's location starts with or refers to 'coder' as the top-level folder (for example, 'coder' alone, or 'coder/something', in any capitalization), treat this as meaning /home/coder — prepend /home in front of it, and do not add an extra 'coder' folder underneath. Third, for any other relative location the user gives, pass it exactly as described, with no leading slash added or removed by you. Once you have determined the correct raw location using these rules, always call resolve_absolute_path first with that value, and use the exact result it returns as the path argument for any subsequent tool call — never modify, guess, or construct the final absolute path yourself. More generally, if the user's request is missing any necessary details — for a path or otherwise — do not call a tool; ask a clarifying question first instead."}
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