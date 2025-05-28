import ollama
from retriever import retrieve_top_k

MODEL_NAME = "gemma3:latest"


def build_prompt(query, retrieved_chunks):
    context_texts = "\n\n".join(
        f"[{chunk['metadata'].get('source', '')} - {chunk['metadata'].get('page_slide', '')}]\n{chunk['document']}"
        for chunk in retrieved_chunks
    )

    return f"""You are a helpful technical interview tutor.

Use the following context to answer the user's question:

{context_texts}

Question: {query}

Answer in a clear, concise, and beginner-friendly way.
"""


def generate_answer(query):
    retrieved_chunks = retrieve_top_k(query)
    prompt = build_prompt(query, retrieved_chunks)

    response = ollama.chat(
        model=MODEL_NAME, messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    query = input("❓ Enter your question: ")
    answer = generate_answer(query)
    print("\n💡 Answer:\n", answer)
