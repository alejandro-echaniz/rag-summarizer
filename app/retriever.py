# retreiver.py

import chromadb
from embedding_store import create_embeddings
from config import OPENAI_API_KEY

class Retriever:

    def __init__(self, db_path: str = "./chroma_db", collection_name: str = "pdf_embeddings"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(collection_name)

    def query(self, query: str, top_k: int = 5) -> list:
        try:
            query_embedding = create_embeddings(query)

            # guard clause
            if not query_embedding:
                print(f'Failure to generate query embeddings')
                return []
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            if not results or not results['documents']:
                print("No matching documents found.")
                return []
            
            # Extract and format the documents and metadata
            documents = []
            for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                documents.append({
                    "text": doc,
                    "metadata": meta
                })

            return documents

        except Exception as e:
            print(f'(ERROR) retriever.py -> query(): {e}')
