import ollama
from src.retriever import Retriever


class Generator:
    def __init__(self, model_name="gemma3:latest", top_k=10):
        self.model_name = model_name
        self.retriever = Retriever(top_k=top_k)

    def build_prompt(self, query, retrieved_chunks):
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

    def generate_answer(self, query):
        retrieved_chunks = self.retriever.retrieve_top_k(query)
        prompt = self.build_prompt(query, retrieved_chunks)

        response = ollama.chat(
            model=self.model_name, messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    def run(self):
        query = input("❓ Enter your question: ")
        answer = self.generate_answer(query)
        print("\n💡 Answer:\n", answer)


if __name__ == "__main__":
    generator = Generator()
    generator.run()
