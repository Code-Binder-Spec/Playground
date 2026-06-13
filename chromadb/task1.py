import chromadb
from groq import Groq
client = chromadb.PersistentClient(path="task1.db")
collection = client.get_or_create_collection("task1")
question = "Who is barbie ?"

if collection.count() == 0 :
    collection.add(
        documents=["Adhil is a programmer who work hard for his goals.","Messi is a world class football player who achieved world cup.","Spider man is marvel superhero who endure great sacrifices."],
        ids=["1","2","3"]
    )

result = collection.query(
    query_texts=[question],
    n_results=1
   )
chunk = result["documents"][0][0]
groq_client = Groq(api_key="cant show in github")
message = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=1024,
    messages= [
        {"role":"user","content": f"Context : {chunk}\n\nInstructions : Only answer from the context. if the answer is not in context say i dont know\n\nQuestion : {question}"}
    ]
)
print(message.choices[0].message.content)
