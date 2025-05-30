import json
from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
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
        chunks = []
        with open(self.chunks_file, "r", encoding="utf-8") as f:
            for line in f:
                chunks.append(eval(line))
        return chunks

    def embed_chunks(self, chunks):
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
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved {len(data)} embedded items to {self.output_file}")

    def update_processed_chunks_file(self):
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
        chunks = self.load_chunks()
        chunks_to_embed, embeddings, offset = self.embed_chunks(chunks)
        data = self.prepare_data_for_vector_store(chunks_to_embed, embeddings, offset)
        self.save_embeddings_to_json(data)
        self.update_processed_chunks_file()
        print("✅ All Embedder operations completed successfully.")


if __name__ == "__main__":
    embedder = Embedder()
    embedder.run_pipeline()
