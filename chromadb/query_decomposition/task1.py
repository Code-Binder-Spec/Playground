import chromadb
import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient("decomposition.db")
collection = client.get_or_create_collection("decomposition")

if collection.count() == 0:
    collection.add(
        documents=["Engineer is the one who solve problems and fix everything.","Doctor is one who treat patients kindly and help us to recover from disease","Discipline person is who works hard for his goals through structure and shedules he will be consistent even when he dont want to do the things"],
        ids=["1","2","3"]
    )

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

while True:
    query = str(input(" YOU : "))
    if "stop" in query :
        break
    result = collection.query(
        query_texts=[query],
        n_results=1
    )
    chunk = result["documents"][0][0]
    message = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
               {"role":"user","content":f"context : {chunk}\n\ninstructions : Answer only from context if answer is not in context say i dont know.\n\nQuestion : {query}"}
        ]
    )
    print(f" lllolollloooAI : {message.choices[0].message.content}")

