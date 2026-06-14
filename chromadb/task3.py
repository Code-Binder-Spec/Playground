import chromadb
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient("allu.db")
collection = client.get_or_create_collection("allu")

if collection.count() == 0:
    with open("C:/Users/adhim/OneDrive/Desktop/cousins_data.txt","r+") as f:
        data = f.read().strip()
        data_list = data.split("-")
    collection.add(
        documents=[data for data in data_list],
        ids = [f"{i}" for i in range(1,(len(data_list)+1))],
        metadatas=[{"Name":"Azil"},{"Name":"Amna"},{"Name":"Aqil"},{"Name":"Arya"},{"Name":"Anna"}]
    )

print("\n Type stop in query to exit \n")

messages_lis = []
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
messages_lis.append({"role": "system", "content": "Answer only from the context provided. If the answer is not in the context, say 'I don't know'. Always refer to the person by their name. If the user only mentions a name without a question, ask 'What would you like to know about {name}?' and wait. If no name is mentioned, ask for it before answering."})
active_name = None

while True:
   
    metadata_v = None
    query = str(input("YOU : "))
    if query.lower() == "stop":
                 break
    else :
                    if "azil" in query.lower():
                                   metadata_v = {"Name":"Azil"}
                                   active_name = "Azil"
                    elif "amna" in query.lower():
                                   metadata_v = {"Name":"Amna"}
                                   active_name = "Amna"
                    elif "aqil" in query.lower():
                                   metadata_v = {"Name":"Aqil"}
                                   active_name = "Aqil"
                    elif "arya" in query.lower():
                                   metadata_v = {"Name":"Arya"}
                                   active_name = "Arya"
                    elif "anna" in query.lower():
                                   metadata_v = {"Name":"Anna"}
                                   active_name = "Anna"
                   
                    if metadata_v is None and active_name is None:
                                    chunk = None
                    elif metadata_v is None and active_name :
                               metadata_v = {"Name":active_name}
                               result = collection.query(
                                                   query_texts=[query],
                                                   where=metadata_v,
                                                   n_results=1
                                               )  
                               chunk = result["documents"][0][0]
                    else :
                                 result = collection.query(
                                        query_texts=[query],
                                        where=metadata_v,
                                        n_results=1
                                               )    
                                 chunk = result["documents"][0][0]   
                    
                    messages_lis.append({"role":"user","content" : f"Context : {chunk}\n\nQuestion : {query}"})
                    message = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=1024,
                    messages=messages_lis
                    )
                    messages_lis.append({"role":"assistant","content":message.choices[0].message.content})
                    print("AI : ",message.choices[0].message.content)