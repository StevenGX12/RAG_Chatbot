import json
from sentence_transformers import SentenceTransformer
from pathlib import Path
import numpy as np

# Constants
CHUNKS_FILE = "./processed_corpus/processed_chunks.jsonl"
MODEL_NAME = "all-MiniLM-L6-v2"

# Load embedding model
model = SentenceTransformer(MODEL_NAME)


def load_chunks(file_path):
    chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(eval(line))  # line is a dict-like string
    return chunks


def embed_chunks(chunks):
    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return embeddings


def prepare_data_for_vector_store(chunks, embeddings):
    data = []
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        item = {
            "id": f"chunk_{i}",
            "embedding": emb.tolist(),
            "document": chunk["content"],
            "metadata": chunk["metadata"],
        }
        item["metadata"]["type"] = chunk["type"]
        data.append(item)
    return data


def save_embeddings_to_json(
    data, output_path="./processed_corpus/embedded_chunks.json"
):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {len(data)} embedded items to {output_path}")


if __name__ == "__main__":
    chunks = load_chunks(CHUNKS_FILE)
    embeddings = embed_chunks(chunks)
    data = prepare_data_for_vector_store(chunks, embeddings)
    save_embeddings_to_json(data)
