from groq import Groq
from dotenv import load_dotenv
import os
import chromadb

load_dotenv() 

def keyword_matching_function(query,chunk):
        score = 0
        lis_query =  query.lower().split()
        lis_chunk = chunk.lower().split()
        for word in lis_chunk:
                if word in lis_query:
                        score += 1
                else:
                        continue
        return score
        

client = chromadb.PersistentClient("Normal.db")
collection = client.get_or_create_collection("normal")

if collection.count() == 0 :
    collection.add(
        documents=["Timer is not working.","Time is moving","You only have limited time."],
        ids=["1","2","3"]
    )
    
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("\n Type stop in you for exitting \n")
while True :
                 query = str(input(" YOU : "))
                 if "stop" in query.lower():
                         break
                 result = collection.query(
                         query_texts=[query],
                         n_results=3
                 )
                 chunks = result["documents"][0]
                 scores = []
                 for chunk in chunks:
                         keyword_score = keyword_matching_function(query,chunk)
                         scores.append(keyword_score)
                 distances = result["distances"][0]
                 updated_score = [0  if score==0 else score/max(scores) for score in scores]
                 pending_update_distance = [0  if d==0 else d/max(distances) for d in distances]
                 updated_distances = [0 if d==0 else 1-d for d in pending_update_distance]
                 sum_list = []
                 for i in range(len(chunks)):
                         sum_score = updated_score[i] + updated_distances[i]
                         sum_list.append(sum_score)
                 max_number = 0
                 position = 0
                 for i in range(len(chunks)):
                         if sum_list[i] > max_number:
                                 max_number = sum_list[i]
                                 position = i
                         else :
                                 continue
                 real_data_for_retreival = chunks[position]
                 print(chunks)
                 print("keyword scores:", scores)
                 print("normalized keyword:", updated_score)
                 print("distances:", distances)
                 print("normalized distance:", updated_distances)
                 print("sum:", sum_list)
                 print(real_data_for_retreival)
                 message = groq_client.chat.completions.create(
                             model="llama-3.3-70b-versatile",
                             max_tokens=1024,
                             messages=[
                                           {"role":"user","content" : f"Context : {real_data_for_retreival}\n\nInstructions : Answer properly from the context.\n\nQuestion :{query}"}
                                                ]
                                       )
                 print(f" AI : {message.choices[0].message.content}")
                 