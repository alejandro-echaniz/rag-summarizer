# summarizer.py

import openai
from config import OPENAI_API_KEY
from retriever import Retriever

openai.api_key = OPENAI_API_KEY

class Summarizer:

    def __init__(self, model: str = 'gpt-4-turbo', ):
        self.model = model
        self.retriever = Retriever()

    def generate_prompt(self, documents: list) -> str:

        prompt = "You are an expert summarizer. Summarize the following information into a concise and clear overview:\n\n"

        for idx, doc in enumerate(documents):
            prompt += f"### Document {idx + 1}\n"
            prompt += f"Text: {doc['text']}\n"
            prompt += f"Metadata: {doc['metadata']}\n\n"

        prompt += "\nProvide a clear, coherent summary highlighting the main points."
        return prompt

    def summarize(self, query: str, top_k: int = 5) -> str:
        try:
            print("\n Retrieving similar documents...")
            documents = self.retriever.query(query, top_k)

            if not documents:
                return "No relevant documents found."

            print("\n Generating prompt...")
            prompt = self.generate_prompt(documents)

            print("\n Sending prompt to LLM for summarization...")
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful summarizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            # Extract and return the summary
            summary = response['choices'][0]['message']['content']
            return summary

        except Exception as e:
            print(f"(ERROR) summarizer.py -> summarize(): {e}")
            return "An error occurred during summarization."
