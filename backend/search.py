from backend.embedding import get_model
from backend.vector_store import search
def retrieve_chunks(question,filenames=None):
    model=get_model()
    query_embedding=model.encode(question)
    results=search(query_embedding,filenames)
    print(results["documents"])
    return results