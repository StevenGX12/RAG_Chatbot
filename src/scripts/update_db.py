from src.data_loader import DataLoader
from src.embedder import Embedder
from src.vector_store import VectorStoreManager


def update_pipeline():
    print("🚀 Starting update pipeline...")

    # Step 1: Load and process any new files from corpus
    print("📂 Loading and processing new files from corpus...")
    loader = DataLoader()
    loader.run_pipeline()

    # Step 2: Embed unembedded chunks
    print("🔍 Embedding unembedded chunks...")
    embedder = Embedder()
    embedder.run_pipeline()

    # Step 3: Add new embeddings to vector store
    print("🗃️ Adding new embeddings to vector store...")
    vector_store_manager = VectorStoreManager()
    vector_store_manager.run_pipeline()


if __name__ == "__main__":
    update_pipeline()
