import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Constants
VECTOR_STORE_PATH = "./chroma_store"
COLLECTION_NAME = "interview-prep"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5

# Load embedding model
embedder = SentenceTransformer(MODEL_NAME)

# Set up ChromaDB client
client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)

# Load collection
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def embed_query(query: str):
    return embedder.encode(query, convert_to_numpy=True).tolist()


def retrieve_top_k(query: str, top_k=TOP_K):
    query_embedding = embed_query(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append(
            {
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )
    return retrieved


if __name__ == "__main__":
    # Test query
    query = input("🔍 Enter your query: ")
    results = retrieve_top_k(query)
    for r in results:
        print("\n---")
        print(f"[{r['metadata'].get('source')}] {r['metadata'].get('page_slide', '')}")
        print(r["document"])
