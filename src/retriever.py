import chromadb
from sentence_transformers import SentenceTransformer


class Retriever:
    """
    A class for retrieving top-k relevant documents from a vector store using sentence embeddings.
    This class uses a SentenceTransformer model to embed queries and retrieves the most relevant documents
    from a persistent ChromaDB vector store collection.
    Attributes:
        top_k (int): Default number of top results to retrieve.
        model (SentenceTransformer): The embedding model used for queries.
        client (chromadb.PersistentClient): The persistent ChromaDB client.
        collection (chromadb.Collection): The collection within the vector store.

        Initializes the Retriever with a vector store, collection, and embedding model.

    Args:
        vector_store_path (str, optional): Path to the persistent vector store. Defaults to "./chroma_store".
        collection_name (str, optional): Name of the collection in the vector store. Defaults to "interview-prep".
        model_name (str, optional): Name of the SentenceTransformer model to use. Defaults to "all-MiniLM-L6-v2".
        top_k (int, optional): Default number of top results to retrieve. Defaults to 10.
    """

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
        """
        Embeds a query string into a vector using the SentenceTransformer model.
        Args:
            query (str): The input query string to embed.
        Returns:
            list: The embedding vector of the query as a list of floats.
        """
        return self.model.encode(query, convert_to_numpy=True).tolist()

    def retrieve_top_k(self, query: str, top_k=None):
        """
        Retrieves the top-k most relevant documents for a given query.
        Args:
            query (str): The input query string.
            top_k (int, optional): Number of top results to retrieve. If None, uses the default top_k.
        Returns:
            list: A list of dictionaries, each containing 'id', 'document', 'metadata', and 'distance' for a result.
        """
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
        """
        Prompts the user for a query, retrieves the top-k relevant documents, and prints them.
        This method interacts with the user via the command line.
        """
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
