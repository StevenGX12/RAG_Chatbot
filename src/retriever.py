import chromadb
from sentence_transformers import SentenceTransformer


class Retriever:
    def __init__(
        self,
        vector_store_path="./chroma_store",
        collection_name="interview-prep",
        model_name="all-MiniLM-L6-v2",
        top_k=10,
    ):
        self.top_k = top_k
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=vector_store_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def embed_query(self, query: str):
        return self.model.encode(query, convert_to_numpy=True).tolist()

    def retrieve_top_k(self, query: str, top_k=None):
        if top_k is None:
            top_k = self.top_k
        query_embedding = self.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )
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

    def run_query(self):
        query = input("🔍 Enter your query: ")
        results = self.retrieve_top_k(query)
        for r in results:
            print("\n---")
            source = r["metadata"].get("source", "Unknown")
            page_slide = r["metadata"].get("page_slide", "")
            print(f"[{source}] {page_slide}")
            print(r["document"])


if __name__ == "__main__":
    retriever = Retriever()
    retriever.run_query()
