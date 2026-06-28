from backend.embedding import model
from backend.vector_store import search
def retrieve_chunks(question,filename=None):
    query_embedding=model.encode(question)
    results=search(query_embedding,filename)
    print(results["documents"])
    return results