import json

INPUT_FILE = "./processed_corpus/embedded_chunks.jsonl"


def backfill_embedded_flag(input_path):
    updated_chunks = []

    # Read and update all lines
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            chunk = eval(line.strip())  # Deserialize each line
            chunk["metadata"]["embedded"] = True  # Add the embedded flag
            updated_chunks.append(chunk)

    # Overwrite the file with updated content
    with open(input_path, "w", encoding="utf-8") as f:
        for chunk in updated_chunks:
            f.write(f"{repr(chunk)}\n")

    print(f"✅ Backfilled {len(updated_chunks)} chunks with embedded=True")


if __name__ == "__main__":
    backfill_embedded_flag(INPUT_FILE)
