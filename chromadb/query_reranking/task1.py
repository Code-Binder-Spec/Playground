import chromadb
from groq import Groq
import os 
from dotenv import load_dotenv

load_dotenv()


client = chromadb.PersistentClient("reranking.db")
collection = client.get_or_create_collection("reranking")

if collection.count() == 0:
    collection.add(
        documents=["Programmer is the one who solves problem make logic to function script","UI designer is a designer who designs user interface and animation.","Web developer is the creator web pages that can accesed through internet","Buisness owner is a person who have a company or product that influences peoples life."],
        ids=["1","2","3","4"]
    )

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("\n type stop in You for existting. \n")

while True:
    query = str(input(" YOU : "))
    result  = collection.query(
        query_texts=[query],
        n_results=4
    )
    chunks = result["documents"][0]
    message_1 = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role":"system","content":f"Retrived data : {[f"{i}.{chunk}" for i,chunk in enumerate(chunks)]}\n\nInstructions : Say the two best-matching option numbers for the query. Output only the two option numbers.No space between option numbers except coma.\n\nQuestion : {query}"}
        ]
    )
    indexes = message_1.choices[0].message.content
    lis_indexes = indexes.split(",")
    real_chunk = []
    for i in lis_indexes:
             real_chunk.append(chunks[int(i)])
    message_2  = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role":"user","content":f"context : {real_chunk}\n\nInstructions : Answer only from context and it should be proper . if answer is not in context say i dont know.\n\nQuestion : {query}"}
        ]
    )
    print(f" AI : {message_2.choices[0].message.content}")