import ollama
from src.retriever import Retriever


class Generator:
    """
    A class for generating answers to user queries using a retrieval-augmented generation (RAG) approach.
    This class retrieves relevant document chunks based on a user query and constructs a prompt for a language model to generate a helpful, beginner-friendly answer.
    Args:
        model_name (str, optional): The name of the language model to use. Defaults to "gemma3:latest".
        top_k (int, optional): The number of top relevant chunks to retrieve. Defaults to 10.
    """

    def __init__(self, model_name="gemma3:latest", top_k=10):
        self.model_name = model_name
        self.retriever = Retriever(top_k=top_k)

    def build_prompt(self, query, retrieved_chunks):
        """
        Builds a prompt for the language model using the user query and retrieved document chunks.
        Args:
            query (str): The user's question.
            retrieved_chunks (list): A list of retrieved document chunks, each containing 'document' and 'metadata'.
        Returns:
            str: The constructed prompt for the language model.
        """
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
        """
        Generates an answer to the user's query using retrieved context and the language model.
        Args:
            query (str): The user's question.
        Returns:
            str: The generated answer from the language model.
        """
        retrieved_chunks = self.retriever.retrieve_top_k(query)
        prompt = self.build_prompt(query, retrieved_chunks)

        response = ollama.chat(
            model=self.model_name, messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    def run(self):
        """
        Runs the generator, prompting the user for a question and generating an answer.
        This method handles user input and displays the generated answer.
        """
        query = input("❓ Enter your question: ")
        answer = self.generate_answer(query)
        print("\n💡 Answer:\n", answer)


if __name__ == "__main__":
    generator = Generator()
    generator.run()
