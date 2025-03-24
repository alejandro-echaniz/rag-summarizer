# **<u>RAG-Flow For PDF Summarizations</u>**
*By Alejandro Echaniz*

![Basic RAG flowchart](https://miro.medium.com/v2/resize:fit:1400/1*sJU5gG7CRdNsn3v3CSSQFg.png)

## ***Overview***
Retrieval-Augmented Generation (i.e. RAG) is a technique improving accuracy and 
quality of large language models (LLMs) by combining *retrieval* and *generation*
Through the accessibility of an external knowledge (PDF content, databases) during
the query time, more precise and factually relavant output can be displayed.

In this project, RAG-flow is utilized to summarize PDFs. It begins by taking 
text from PDFs and storing them in ChromaDB. It uses the `ingest` command to 
fetch text from PDFs and store an embedding per section using the OpenAI API. 
When someone submits a question through the `query` command, the retriever 
retrieves the appropriate sections of the document from ChromaDB with the 
corresponding question's embedding. The summarizer then constructs a brief 
summary using a language model, including the retrieved material to provide a 
more relevant and clear summary.

## ***Project Layout***
### **Directory**
```{md}rag-summarizer/
├─ app/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ pdf_processor.py
│  ├─ embedding_store.py
│  ├─ config.py
│  ├─ retriever.py
│  ├─ summarizer.py
├─ data/
├─ requirements.txt
├─ README.md
```

### **Packages**
| Name | Version | Purpose |
|:-------------|---------|---------|
| [ChromaDB](https://docs.trychroma.com/docs/overview/introduction) | 0.6.3 | Embedding Database |
| [click](https://click.palletsprojects.com/en/stable/) | 8.1.7 | Seamless CLI functionality |
| [openai](https://platform.openai.com/docs/overview) | 0.28.0 | Embedding & Summarization models |
| [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) | 1.25.4 | Efficient PDF processing/parsing|
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.0.1 | Loading environmental variables into Python environment |

### **Application Workflow**
```{md}
                          CLI Interface (cli.py)
                                    │
                                    ▼
                ┌───────────────────────────────────┐
                │                                   │
            Parse PDF                       Retrieve Embeddings
       (pdf_processor.py)                     (retriever.py)
                │                                   │
                ▼                                   ▼
            Embed PDF                        Retrieve Chunks
      (embedding_store.py)                   (from ChromaDB)
                │                                   │
                ▼                                   ▼
      Store Embeddings in                  Summarize with LLM
            ChromaDB                         (summarizer.py)

```

---

## ***Running the Application***
Before using the CLI, ensure the following:
- Python 3.7 or higher installed
- Install the required dependencies by running:
```bash
  pip install -r requirements.txt
```
- A .env file in the root directory containing your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key
```

There are two commands to run wihtin the application: `ingest` and `query`.
1. Ingest a PDF:
    - Use the `ingest` command to process the PDF and store embeddings.
2. Query for information:
    - Use the `query` command to retrieve and summarize relevant documents based on your query.

### **Ingesting**
This command extracts text from a PDF file, generates embeddings, and stores 
them in a ChromaDB collection.

```bash
python cli.py ingest <pdf_path> --source <source_name> --author <author_name> [--output_path <output_path>]
```
- `<pdf_path>`: Path to the PDF file you want to process.
- `--source`: The source name (e.g., document title). 
- `--author`: The author's name
- `--output path`: the file path where the extracted text will be stored 
(default is output.txt).

#### Ingest Sample Command
```bash
python cli.py ingest data/example_checkers.pdf --source "Checkers Rules" --author "John Doe" --output_path output.txt
```
This command will extract text from the example_checkers.pdf file, store it in output.txt, generate embeddings, and save them to ChromaDB.


### **Querying**
This command retrieves the most relevant documents from the database based on the user’s query and provides a summary using an LLM.

```bash
python cli.py query <query> [--top_k <top_k>]
```
- `<query>`: The search query for retrieving documents.
- `--top_k`: The number of similar documents to retrieve (default is 5).

#### Query Sample Command
```bash
python cli.py query "What are the rules of checkers?" --top_k 3
```
This will retrieve and summarize the top 3 documents related to the query "What are the rules of checkers?".