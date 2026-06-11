import chromadb

cleint = chromadb.PersistentClient(path="test_db")
collection = cleint.get_or_create_collection("test")
collection.add(
    documents=["i love prograaming","coding is crazy","python is the best"],
    ids=["1","2","3"]
)
result = collection.query(
    query_texts=["i like coding"],
    n_results=2
)
print(collection.get())