from mcp.client.stdio import stdio_client
from mcp import ClientSession,StdioServerParameters
import asyncio
import groq
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from groq import Groq

final_answer = None

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY_1"))


def calculating_total_char_of_messages(messages):
        listed_string = []
        for item in messages:
                stringed_item = str(item)
                listed_string.append(stringed_item)
        joined_string = "".join(listed_string)
        total_char_in_messages = len(joined_string)
        return total_char_in_messages

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

def getting_limit_char_of_model(response):
        token_limit = int(response.headers.get("x-ratelimit-limit-tokens", 0))
        approx_char = token_limit * 3
        return approx_char

def checking_limit(messages,response,combined):
        data = None
        stop = False
        char_messages = calculating_total_char_of_messages(messages)
        limit_char_model = getting_limit_char_of_model(response) 
        prompt_char = 1400
        total_char = char_messages + prompt_char
        if total_char > limit_char_model:
                data = ("correct",combined,"Model limit passed : The ai cant verify or structure the data because the request limit is passed by the amount of data . Upgrade the model to higher version for more request tokens")
                stop = True
        if stop:
                return (data,'break')
        else :
                return (data,"continue")
async def actual_agentic_function(messages,groq_tools,session):
        data = None
        while True:
                            raw_response = groq_client.chat.completions.with_raw_response.create(
                                                             model="openai/gpt-oss-120b",
                                                             max_tokens=1024,
                                                             messages=messages,
                                                             tools=groq_tools,
                                                             tool_choice="auto"
                                                                             )
                            response = raw_response.parse()
                            message = response.choices[0].message
                            print(message)
                            messages.append(message)

                            if message.tool_calls:
                                        tool_call = message.tool_calls[0]
                                        result = await session.call_tool(tool_call.function.name,json.loads(tool_call.function.arguments))
                                        combined_text = "\n".join(item.text for item in result.content)
                                        messages.append(
                                                                         {
                                                                             "role":"tool",
                                                                             "tool_call_id":tool_call.id,
                                                                             "content":combined_text
                                                                                              }
                                                                                   )
                                        check = checking_limit(messages,response,combined_text)
                                        if "break" in check:
                                                data = check[1]
                                                break
                                        ai_reply = calling_ai(groq_client,f"You are evaluating whether an AI agent correctly fulfilled a user's request by calling the appropriate tool(s). You will be given the full conversation history, including the user's request, which tools the agent called, with what arguments, and the results returned. Your only job is to judge whether the agent's tool calls functionally satisfied what the user actually asked for. The number of tool calls, which specific tools were used, or the order of calls does not matter — only whether the end result accomplishes what the user needed. If the agent called the correct tool(s) and got a correct result, but never actually concluded with a real, final answer to the user (for example, it stopped after just printing or holding onto the raw tool result, without turning it into an actual response), treat this as DIDNT APPROVED as well, since the task isn't truly finished until the agent gives a real, conclusive answer. If the agent's actions correctly satisfied the user's request, including concluding with a real final answer, respond with exactly: CORRECT. If the agent's actions did NOT satisfy the user's request, respond with: DIDNT APPROVED, followed by a brief, specific reason why.\n\nConversational history : {messages}")
                                        if "CORRECT" in ai_reply:
                                                                        data = ("correct",combined_text,"Correct amount of data within limit")
                                                                        break
                                        else :
                                                                        messages.append({"role":"system","content":f"{ai_reply}"})
                                                                        continue
                            else :
                                    check = checking_limit(messages,response,response.choices[0].message.content)
                                    if "break" in check:
                                            data = check[1]
                                            break
                                    ai_reply1 = calling_ai(groq_client,f"You are evaluating whether an AI agent correctly fulfilled a user's request by calling the appropriate tool(s). You will be given the full conversation history, including the user's request, which tools the agent called, with what arguments, and the results returned. Your only job is to judge whether the agent's tool calls functionally satisfied what the user actually asked for. The number of tool calls, which specific tools were used, or the order of calls does not matter — only whether the end result accomplishes what the user needed. If the task was stopped because of a permission error (the agent was correctly blocked from an unauthorized action), treat this as CORRECT, since the agent behaved as intended by respecting the restriction — respond with exactly: CORRECT, and tell the agent to conclude by explaining the permission error to the user. If the agent's actions correctly satisfied the user's request, respond with exactly: CORRECT. If the agent's actions did NOT satisfy the user's request, respond with exactly: DIDNT COMPLETED, followed by a brief reason why.\n\nConversational history : {messages}")
                                    if "CORRECT" in ai_reply1:
                                            data = ("correct",response.choices[0].message.content,"Correct amount of data within limit")
                                            break
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
                                                                                {"role": "system", "content": f"Whenever a task requires a file or folder, follow these rules. If the user refers to their home directory by itself (with no further location specified), use exactly this path: {string_home} . If the user's request goes beyond just the home directory — naming a specific file or folder inside it — call finding_real_paths_of_entry with just that name (not a full path). Otherwise, for any task requiring a file or folder, always call finding_real_path_of_entry first with just the name before calling any other tool. finding_real_path_of_entry only ever requires one thing: the final name being searched for — even if the user mentions parent folders or a longer path, extract only the last, final name from what they said and pass just that single name; do not pass any parent folders or path segments along with it. Do not try to assume, guess, or construct any path yourself — always rely on finding_real_path_of_entry to determine the correct path. If it returns a single path, use that exact path for the next tool call. If it returns multiple matches, do not proceed — list the matches for the user and ask which one they mean, then use their answer to select the correct path before calling the next tool. If it returns that the path doesn't exist, tell the user and do not proceed with any further tool call. If the user is only asking how many paths exist for a given folder or file name, simply conclude with the result of the function — do not proceed to call any other tool."}
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
                                                                                                              messages_num = calculating_total_char_of_messages(messages)
                                                                                                              print(f"total_char in messages = {messages_num}")
                                                                                                              ai_reply = calling_ai(groq_client,f"You are evaluating an AI agent's latest response in a conversation. Determine whether the agent is currently expecting more information or an answer from the user before it can continue or complete the task, or whether it is not expecting anything further from the user right now. If the agent is asking a question or otherwise waiting on information or a decision from the user, respond with exactly: QUESTION. If the agent is not asking anything or waiting on any information or answer from the user — including if the latest response is simply a plain answer, regardless of who or what it came from — respond with exactly: STOP. The full conversational history will be given.\n\nConversational history : {messages}")
                                                                                                              if "QUESTION" in ai_reply:
                                                                                                                         data =  result[1]
                                                                                                                         continue
                                                                                                              else :
                                                                                                                       print(f"{result[1]} \n : agents job done :",result[2])
                                                                                                                       break
                                                                                                  elif "again" in result:
                                                                                                                          data = result[1]
                                                                                                                          continue

asyncio.run(main())