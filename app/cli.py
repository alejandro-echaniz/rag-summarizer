# cli.py

import click
import os

from pdf_processor import extract_text_from_pdf
from embedding_store import store_embeddings
from retriever import Retriever
from summarizer import Summarizer

# Define the default output path
DEFAULT_OUTPUT_PATH = "output.txt"

@click.group()
def cli():
    """CLI for RAG Summarizer"""
    pass

@click.command()
@click.argument('pdf_path')
@click.option('--source', required=True, help="Source of the document")
@click.option('--author', required=True, help="Author of the document")
@click.option('--output_path', default=DEFAULT_OUTPUT_PATH, help="Path to save the extracted text")
def ingest(pdf_path, source, author, output_path):
    # Extract text from PDF
    extract_text_from_pdf(pdf_path, output_path)
    
    # Read the extracted text from the output file
    with open(output_path, 'r', encoding="utf-8") as file:
        text = file.read()
    
    # Store embeddings with metadata
    metadata = {"source": source, "author": author}
    store_embeddings(text, metadata)

    print(f"Successfully ingested and stored embeddings for {pdf_path}")

@click.command()
@click.argument("query")
@click.option("--top_k", default=5, help="Number of similar documents to retrieve")
def query(query, top_k):
    summarizer = Summarizer()

    print(f"\nRetrieving and summarizing documents for query: {query}")
    summary = summarizer.summarize(query, top_k)

    print("\n--- Summary ---")
    print(summary)

cli.add_command(ingest)
cli.add_command(query)

if __name__ == '__main__':
    cli()