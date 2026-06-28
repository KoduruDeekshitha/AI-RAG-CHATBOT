import chromadb
client=chromadb.PersistentClient(path="chroma_db")
collection=client.get_or_create_collection(name="documents")
def store_embeddings(chunks,embeddings,filename):
    ids=[]
    metadatas=[]
    for i in range(len(chunks)):
        ids.append(f"{filename}_{i}")
        metadatas.append({"filename":filename})
    collection.add(ids=ids,documents=chunks,embeddings=embeddings.tolist(),metadatas=metadatas)
    return len(ids)
def search(query_embedding,filename=None,n_results=5):
    if filename:
        return collection.query(
            query_embeddings=[query_embedding.tolist()],
            where={"filename":filename},
            n_results=n_results
        )
    return collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )
def delete_file(filename):
    results=collection.get(where={"filename":filename})
    ids=results["ids"]
    if ids:
        collection.delete(ids=ids)
        return len(ids)
    return 0
