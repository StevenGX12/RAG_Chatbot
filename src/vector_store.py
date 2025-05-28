import json
import chromadb

# Constants
VECTOR_STORE_PATH = "./chroma_store"
EMBEDDED_FILE = "./processed_corpus/embedded_chunks.json"
COLLECTION_NAME = "interview-prep"

# Set up ChromaDB client with local persistence
client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)


def load_embedded_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def populate_vector_store(data):
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # Split into batches if needed (for large data)
    ids = [item["id"] for item in data]
    embeddings = [item["embedding"] for item in data]
    documents = [item["document"] for item in data]
    metadatas = [item["metadata"] for item in data]

    collection.add(
        ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
    )
    print(f"✅ Indexed {len(data)} items into ChromaDB collection: '{COLLECTION_NAME}'")


if __name__ == "__main__":
    embedded_data = load_embedded_data(EMBEDDED_FILE)
    populate_vector_store(embedded_data)
