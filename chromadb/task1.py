import chromadb
from groq import Groq
client = chromadb.PersistentClient(path="task2.db")
collection = client.get_or_create_collection("task2")
question = "Who is adhil?"

result = collection.query(
    query_texts=[question],
    n_results=1
   )
chunk = result["documents"][0][0]
groq_client = Groq(api_key="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")
message = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=1024,
    messages= [
        {"role":"user","content": f"Context : {chunk}\n\n Question : {question}"}
    ]
)
print(message.choices[0].message.content)
