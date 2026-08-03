from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_reply(prompt):
    reply = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role":"user","content":f"Instructions : answer properly based on the query\n\nQuery : {prompt}"}
        ]
    )
    return reply.choices[0].message.content

print("type stop in query for quitting")
you = str(input("YOU : "))
while True:
    
    if "stop" in you.lower() :
         break

    agent_a_output = ai_reply(you)
    print(f"\nAGENT A'S ANSWER : {agent_a_output}")
    agent_b_output = ai_reply(f"Here is a draft answer: {agent_a_output}. Point out one flaw or say APPROVED if there isn't one.No need to include the word APPROVED if its not correct")
    print(f"\nAGENT B'S STATUS ON THE OUTPUT OF AGENT A : {agent_b_output}")
    if "approved" in agent_b_output.lower():
         break
    else :
             you = (
                           f"Original answer:\n{agent_a_output}\n\n"
                           f"Critique:\n{agent_b_output}\n\n"
                           f"Please revise the original answer to address the critique above. "
                           f"Return only the revised answer."
                  ) 







