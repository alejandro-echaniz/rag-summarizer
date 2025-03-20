# pdf_processor.py
'''

'''

import fitz 

def extract_text_from_pdf(pdf_path: str, output_path: str) -> str :
    try:
        with fitz.open(pdf_path) as doc:
            out = open("output.txt", "wb")
            
            for page in doc:
                text = page.get_text().encode("utf8")
                out.write(text) 
                out.write(bytes((12,))) 
            out.close() 

    except Error as e:
        print(f'(pdf_processing.py) ERROR Processing pdf: {e}')        

