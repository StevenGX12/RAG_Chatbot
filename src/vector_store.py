import json
import chromadb


class VectorStoreManager:
    def __init__(
        self,
        vector_store_path="./chroma_store",
        embedded_file="./processed_corpus/embedded_chunks.json",
        collection_name="interview-prep",
    ):
        self.embedded_file = embedded_file
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=vector_store_path)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

    def load_embedded_data(self):
        with open(self.embedded_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def populate_vector_store(self, data):
        data_for_indexing = [
            item for item in data if not item["metadata"].get("saved_to_db", False)
        ]
        if not data_for_indexing:
            print("No new data to index in ChromaDB.")
            return

        ids = [item["id"] for item in data_for_indexing]
        embeddings = [item["embedding"] for item in data_for_indexing]
        documents = [item["document"] for item in data_for_indexing]
        metadatas = [item["metadata"] for item in data_for_indexing]

        self.collection.add(
            ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
        )
        print(
            f"✅ Indexed {len(data_for_indexing)} items into ChromaDB collection: '{self.collection_name}'"
        )

    def update_saved_flag(self):
        updated_chunks = []
        update_count = 0
        with open(self.embedded_file, "r", encoding="utf-8") as f:
            embedded_data = json.load(f)
            for chunk in embedded_data:
                if not chunk["metadata"].get("saved_to_db", False):
                    chunk["metadata"]["saved_to_db"] = True
                    update_count += 1
                updated_chunks.append(chunk)

        with open(self.embedded_file, "w", encoding="utf-8") as f:
            json.dump(updated_chunks, f, indent=2)

        print(
            f"✅ Updated 'saved_to_db' flag for {update_count} chunks in {self.embedded_file}"
        )

    def run_pipeline(self):
        data = self.load_embedded_data()
        self.populate_vector_store(data)
        self.update_saved_flag()
        print("✅ Vector store populated and flags updated successfully.")


if __name__ == "__main__":
    manager = VectorStoreManager()
    manager.run_pipeline()
