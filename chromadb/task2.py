import chromadb
from groq import Groq

client = chromadb.PersistentClient("task2.db")
collection_movie = client.get_or_create_collection("movies")
collection_book =client.get_or_create_collection("books")

if collection_book.count() == 0:
           collection_book.add(
                documents=["Atomic habits : A book that help us for building remarkable result by compounding small habits and improvements","Rich dad Poor dad : A book that Help us to understand money principles","Subtitle art of not giving a fu*k : A book that remind us what deserve our energy and what dont it also teaches about You have limited time and be careful to choose.","Deep work : A book help us to understand the power of distraction less focused work and why it produces massive result.","The Alchemist : A book about the story of a sphered boy who follows his dreams and discovers his meaning of his personal legend"],
                ids=["1","2","3","4","5"]
                   )
if collection_movie.count() == 0 :
                     collection_movie.add(
                          documents=["Interstellar : Movie about space and diffrent things far from the earth","Mersal : A thalapthy film that encourages kindness","Social Network : A movie inspired by mark zuckerburg in the theme of programming","Your name : A romance anime movie That shows deep feelings","pele : Movie inpsired by footballer pele for encouraging football fans"],
                          ids=["1","2","3","4","5"]
                     )

question_movie = "Im interested in football which movie should i watch ?"
question_book = "I am guy who interested in improvemest i want to achieve my goals through effort. which book should i read"

result_movie = collection_movie.query(
    query_texts=[question_movie],
    n_results=1
)

result_book = collection_book.query(
        query_texts=[question_book],
        n_results=2
)

chunk_movie = result_movie["documents"][0][0]
chunk_book_list = result_book["documents"][0]
chunk_book = '\n\n'.join(chunk_book_list)

groq_client = Groq(api_key="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")
message = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=1024,
    messages = [
        {"role" : "user" , "content" : f"Instructions : Answer only from the context if answer not in the context say i dont know . if the question have 2 answer in context say both explicitly. Movie Context : {chunk_movie}\n\nBook Context : {chunk_book}.Movie Question : {question_movie}. Book question : {question_book}"}
    ]
)
print(message.choices[0].message.content)

