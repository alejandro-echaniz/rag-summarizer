# pdf_processor.py

import fitz 

def extract_text_from_pdf(pdf_path: str, output_path: str) -> str:
    try:
        # Open the PDF file
        with fitz.open(pdf_path) as doc:
            # Open the output file in write mode
            with open(output_path, "w", encoding="utf-8") as out:
                # Extract text from each page and write to output file
                for page in doc:
                    text = page.get_text()  # Extract text from the page
                    out.write(text)
                    out.write("\n")  # Optionally add a newline between pages

        print(f"Text successfully extracted to {output_path}")
    except Exception as e:
        print(f'(pdf_processor.py) ERROR Processing PDF: {e}')
