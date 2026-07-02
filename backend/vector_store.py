import chromadb
client=chromadb.PersistentClient(path="chroma_db")
collection=client.get_or_create_collection(name="documents")
def store_embeddings(chunks,embeddings,filename):
    ids=[]
    metadatas=[]
    for i in range(len(chunks)):
        ids.append(f"{filename}_{i}")
        metadatas.append({"filename":filename})
    collection.add(ids=ids,documents=chunks,embeddings=embeddings,metadatas=metadatas)
    return len(ids)
def search(query_embedding, filenames=None, n_results=20):

    if filenames:

        all_docs = []
        all_ids = []
        all_meta = []

        for filename in filenames:

            result = collection.query(
                query_embeddings=[query_embedding.tolist()],
                where={"filename": filename},
                n_results=n_results
            )

            all_docs.extend(result["documents"][0])
            all_ids.extend(result["ids"][0])
            all_meta.extend(result["metadatas"][0])

        return {
            "documents":[all_docs],
            "ids":[all_ids],
            "metadatas":[all_meta]
        }

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
