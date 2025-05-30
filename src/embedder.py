import json
from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    """
    A class for embedding text chunks using a SentenceTransformer model.
    This class loads text chunks from a JSONL file, embeds them using the specified model,
    and saves the embeddings along with metadata to a JSON file.
    It also updates the original chunks file to mark the chunks as embedded.
    Attributes:
        chunks_file (str): Path to the input JSONL file containing text chunks.
        output_file (str): Path to the output JSON file where embedded chunks will be saved.
        model (SentenceTransformer): The SentenceTransformer model used for embedding.
    Methods:
        load_chunks(): Loads text chunks from the specified JSONL file.
        embed_chunks(chunks): Embeds the loaded chunks and returns those that need embedding.
        prepare_data_for_vector_store(chunks, embeddings, offset=0): Prepares data for vector store indexing.
        save_embeddings_to_json(data): Saves the embedded data to a JSON file.
        update_processed_chunks_file(): Updates the original chunks file to mark chunks as embedded.
        run_pipeline(): Executes the entire embedding pipeline.
    """

    def __init__(
        self,
        chunks_file="./processed_corpus/processed_chunks.jsonl",
        output_file="./processed_corpus/embedded_chunks.json",
        model_name="all-MiniLM-L6-v2",
    ):
        self.chunks_file = chunks_file
        self.output_file = output_file
        self.model = SentenceTransformer(model_name)

    def load_chunks(self):
        """
        Loads text chunks from the specified JSONL file.
        Returns:
            list: A list of dictionaries, each representing a text chunk with 'content' and 'metadata'.
        """
        chunks = []
        with open(self.chunks_file, "r", encoding="utf-8") as f:
            for line in f:
                chunks.append(eval(line))
        return chunks

    def embed_chunks(self, chunks):
        """
        Embeds the loaded chunks using the SentenceTransformer model.
        Args:
            chunks (list): A list of dictionaries, each containing 'content' and 'metadata'.
        Returns:
            tuple: A tuple containing:
                - chunks_to_embed (list): List of chunks that need embedding.
                - embeddings (np.ndarray): Numpy array of embeddings for the chunks.
                - already_embedded_count (int): Count of chunks that were already embedded.
        """
        already_embedded_count = 0
        texts_to_embed = []
        chunks_to_embed = []

        for chunk in chunks:
            if not chunk["metadata"].get("embedded", False):
                texts_to_embed.append(chunk["content"])
                chunks_to_embed.append(chunk)
            else:
                already_embedded_count += 1

        embeddings = self.model.encode(
            texts_to_embed, show_progress_bar=True, convert_to_numpy=True
        )
        print(f"✅ Embedded {len(texts_to_embed)} chunks")
        if already_embedded_count > 0:
            print(
                f"⚠️ {already_embedded_count} chunks were already embedded and skipped."
            )
        return chunks_to_embed, embeddings, already_embedded_count

    def prepare_data_for_vector_store(self, chunks, embeddings, offset=0):
        """
        Prepares the data for vector store indexing.
        Args:
            chunks (list): List of chunks to be embedded.
            embeddings (np.ndarray): Numpy array of embeddings for the chunks.
            offset (int, optional): Offset for chunk IDs. Defaults to 0.
        Returns:
            list: A list of dictionaries, each containing 'id', 'embedding', 'document', and 'metadata'.
        """
        data = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            item = {
                "id": f"chunk_{i + offset}",
                "embedding": emb.tolist(),
                "document": chunk["content"],
                "metadata": chunk["metadata"],
            }
            item["metadata"]["type"] = chunk["type"]
            item["metadata"]["embedded"] = True
            item["metadata"]["saved_to_db"] = False
            data.append(item)
        return data

    def save_embeddings_to_json(self, data):
        """
        Saves the embedded data to a JSON file.
        Args:
            data (list): A list of dictionaries containing embedded chunks.
        Returns:
            None
        """
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved {len(data)} embedded items to {self.output_file}")

    def update_processed_chunks_file(self):
        """
        Updates the original chunks file to mark chunks as embedded.
        This method reads the chunks file, updates the 'embedded' metadata field,
        and writes the updated chunks back to the file.
        Returns:
            None
        """
        updated_chunks = []
        update_count = 0
        with open(self.chunks_file, "r", encoding="utf-8") as f:
            for line in f:
                chunk = eval(line.strip())
                if not chunk["metadata"].get("embedded", False):
                    update_count += 1
                    chunk["metadata"]["embedded"] = True
                updated_chunks.append(chunk)

        with open(self.chunks_file, "w", encoding="utf-8") as f:
            for chunk in updated_chunks:
                f.write(f"{repr(chunk)}\n")

        print(f"✅ Updated {update_count} to embedded=True in {self.chunks_file}")

    def run_pipeline(self):
        """
        Executes the entire embedding pipeline:
        1. Loads text chunks from the specified JSONL file.
        2. Embeds the chunks using the SentenceTransformer model.
        3. Prepares the data for vector store indexing.
        4. Saves the embedded data to a JSON file.
        5. Updates the original chunks file to mark chunks as embedded.
        Returns:
            None
        """
        chunks = self.load_chunks()
        chunks_to_embed, embeddings, offset = self.embed_chunks(chunks)
        data = self.prepare_data_for_vector_store(chunks_to_embed, embeddings, offset)
        self.save_embeddings_to_json(data)
        self.update_processed_chunks_file()
        print("✅ All Embedder operations completed successfully.")


if __name__ == "__main__":
    embedder = Embedder()
    embedder.run_pipeline()
