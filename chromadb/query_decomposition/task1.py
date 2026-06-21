import chromadb
import os 
from groq import Groq
import json
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient("decomposition.db")
collection = client.get_or_create_collection("decomposition")

if collection.count() == 0:
    collection.add(
                documents=[
    "The Eiffel Tower was completed in 1889 in Paris, France.",
    "Photosynthesis is the process plants use to convert sunlight into energy.",
    "The Great Wall of China stretches over 13,000 miles.",
    "Albert Einstein developed the theory of relativity in the early 1900s.",
    "Octopuses have three hearts and blue blood.",
    "The Amazon rainforest produces about 20 percent of the world's oxygen.",
    "Shakespeare wrote 37 plays and over 150 sonnets.",
    "The human body has 206 bones in adulthood.",
    "Mount Everest is the tallest mountain above sea level on Earth.",
    "The stock market crash of 1929 triggered the Great Depression.",
    "Bananas are botanically classified as berries.",
    "The speed of light is approximately 299,792 kilometers per second.",
    "Leonardo da Vinci painted the Mona Lisa in the early 16th century.",
    "Honey never spoils if stored properly.",
    "The Titanic sank in 1912 after hitting an iceberg.",
    "A group of flamingos is called a flamboyance.",
    "The Sahara is the largest hot desert in the world.",
    "World War II ended in 1945.",
    "Sharks existed before trees appeared on Earth.",
    "The human brain contains about 86 billion neurons.",
    "Coffee is the second most traded commodity in the world after oil.",
    "The Great Barrier Reef is the largest living structure on Earth.",
    "Beethoven composed his 9th Symphony while completely deaf.",
    "Venus is the hottest planet in our solar system.",
    "The printing press was invented by Johannes Gutenberg around 1440.",
    "Penguins propose to their mates with a pebble.",
    "The Berlin Wall fell in 1989.",
    "Mount Kilimanjaro is the tallest mountain in Africa.",
    "DNA was first discovered by Friedrich Miescher in 1869.",
    "Cleopatra lived closer in time to the moon landing than to the building of the Great Pyramid.",
    "Lightning strikes the Earth about 8 million times per day.",
    "The first computer virus was created in 1983.",
    "Wolves howl to communicate over long distances with their pack.",
    "The Statue of Liberty was a gift from France to the United States.",
    "Mozart began composing music at the age of five.",
    "The Pacific Ocean is the largest and deepest ocean on Earth.",
    "Marie Curie was the first person to win Nobel Prizes in two different sciences.",
    "A bolt of lightning is hotter than the surface of the sun.",
    "The first Olympic Games were held in ancient Greece in 776 BC.",
    "Elephants are the only mammals that cannot jump.",],
                ids=[f"{i}" for i in range(1,41)]
    )

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

while True:
    query = str(input(" YOU : "))
    if "stop" in query.lower() :
        break
    message_1 = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role" : "system","content":f"context : {query}\n\ninstructions :You will receive a user's input, which may contain one or more questions combined together. Your task is to split it into separate, complete, well-formed questions — do NOT answer them. Return ONLY a valid JSON array of strings, one string per question. If the input contains no actual question (for example: a greeting, statement, or random text), return a JSON array containing exactly one string: no question. Return nothing else — no answers, no explanations, no extra text."}
        ]
    )
    decomposed = message_1.choices[0].message.content
    print(decomposed)
    decomposed_list = json.loads(decomposed)
    cleaned_questions = " ".join(decomposed_list)
    decomposed_data = []
    for i in decomposed_list:
             result = collection.query(
                            query_texts=[i],
                            n_results=1
                        )
             chunk = result["documents"][0][0]
             decomposed_data.append(chunk)
    clean_context = "\n\n".join(decomposed_data)
    message_2 = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
               {"role":"user","content":f"context : {clean_context}\n\ninstructions : Answer only from context if answer is not in context say i dont know.if theres multiple question answer for each.response should be celan readable organized output\n\nQuestion : {cleaned_questions}"}
        ]
    )
    print(f" AI : {message_2.choices[0].message.content}")

