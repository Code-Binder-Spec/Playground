import chromadb
#from groq import Groq

client = chromadb.PersistentClient("allu.db")
collection = client.get_or_create_collection("allu")

if collection.count() == 0:
    with open("/C:/Users/adhim/OneDrive/Desktop/cousins_data.txt.txt","r+") as f:
        data = f.read().strip()
        data_list = data.split("-")
    collection.add(
        documents=[data for data in data_list],
        ids = [f"{i}" for i in range(1,(len(data_list)+1))],
        metadata=[{"Name":"Azil"},{"Name":"Amna"},{"Name":"Aqil"},{"Name":"Arya"},{"Name":"Anna"}]
    )

print("Type stop in query to exit \n")
#there is groq api but due to github dont allow it i removed

while True:
    query = str(input("YOU : "))
    if query.lower() == "stop":
                 break
    if "azil" in query.lower():
            metadata_v = [{"Name":"Azil"}]
    else :
                     result = collection.query(
                     query_texts=[query],
                     n_results=1
                                     )
                     chunk = result["documents"][0][0]
                     message = groq_client.chat.completions.create(
                     model="llama-3.3-70b-versatile",
                     max_tokens=1024,
                     messages=[
                      {"role":"user","content": f"Context : {chunk}\n\nInstructions : Every answer should be from context if the answer is not tin the context say i dont know.Every his or he should point to the user by calling name.If user didnt say name in question force them in to add name in question for finding matching answer.\n\nQuestion : {query}"}
                           ])
                     print("AI : ",message.choices[0].message.content)