
# embedding_store.py

import os, uuid, openai, chromadb
from config import OPENAI_API_KEY
from dotenv import load_dotenv

load_dotenv()

openai.api_key = OPENAI_API_KEY

client = chromadb.Client()
collection = client.get_or_create_collection("pdf_embeddings")


def create_embeddings(text: str) -> list:
    try:
        response = openai.Embedding.create(
            model="text-embedding-3-large",
            input=text
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None


def chunk_text(text: str, chunk_size: int = 100):
    words = text.split()
    return [ " ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size) ]


def store_embeddings(text: str, metadata: dict):
    try:
        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):
            embedding = create_embeddings(chunk)

            if not embedding:
                print(f"(ERROR) Failed to generate embedding for chunk {idx}")
                continue
            
            unique_id = str(uuid.uuid4())

            collection.add(
                ids=[unique_id],
                documents=[chunk],
                metadatas=[{
                    **metadata, 
                    "chunk_index": idx,
                    "chunk_size": len(chunk.split())
                }],                       
                embeddings=[embedding]
            )
            
            print(f"Embedding stored successfully for chunk {idx} of {metadata.get('source')}")
            
    except Exception as e:
        print(f"(ERROR) embedding_store.py -> store_embeddings(): error storing embeddings: {e}")

def retrieve_similar_documents(query: str, top_k: int = 5):
    try:
        query_embedding = create_embeddings(query)
        
        if query_embedding:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            return results['documents']  
        else:
            print("Error generating query embedding.")
            return []
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return []
