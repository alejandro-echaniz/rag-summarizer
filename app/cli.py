# cli.py

import click
from pdf_processor import extract_text_from_pdf

@click.command()
@click.argument("pdf_path")
def process_pdf(pdf_path):
    """Extract and display text from a PDF file."""
    extract_text_from_pdf(pdf_path)

if __name__ == "__main__":
    process_pdf()

