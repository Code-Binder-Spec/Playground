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
    agent_b_output =  ai_reply(
    f"Question: {you}\n\n"
    f"Answer to evaluate:\n{agent_a_output}\n\n"
    f"Evaluate this answer strictly against the question. "
    f"Only flag an issue if the answer is factually incorrect, incomplete, "
    f"or fails to actually answer the question. "
    f"Do not suggest stylistic, tone, or minor wording improvements. "
    f"If the answer meets this bar, respond with exactly: APPROVED\n"
    f"If it does not, respond with exactly: NEEDS REVISION, followed by "
    f"a one-sentence explanation of the specific factual or completeness issue."
    f"Return only explanation of critique . NO other outputs"
)
    print(f"\nAGENT B'S STATUS ON THE OUTPUT OF AGENT A : {agent_b_output}")
    if "approved" in agent_b_output.lower():
         break
    else :
             original_query = you
             you = (
                     f"Original question: {original_query}\n\n"
                     f"Original answer:\n{agent_a_output}\n\n"
                     f"Critique:\n{agent_b_output}\n\n"
                     f"Revise the original answer to address the critique above. "
                     f"Return only the revised answer, with no explanation or commentary."
               )
print("honestly dont know what to do again only for showup")







