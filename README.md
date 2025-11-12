# Doxa-Langchain

A small demo project that loads a PDF, creates embeddings with OpenAI, stores them in a FAISS vector store, and builds a LangChain-based retriever QA chain.

This README covers setup (Windows PowerShell), how to run the included modules, troubleshooting tips, and notes about environment variables.

## Project layout

- `app.py` — (optional) top-level runner (check contents).
- `modules/process_pdf.py` — PDF loader and helper to convert a PDF into LangChain `Document` objects.
- `modules/qa_chain.py` — Creates a retriever QA chain from text using FAISS + OpenAI embeddings.
- `docs/` — Place PDFs here (e.g. `clinton_profile.pdf`).

## Requirements

- Python 3.11+ (tested with 3.12 in this workspace)
- Virtual environment (recommended)
- The project uses the following notable packages (installed into the venv):
  - langchain, langchain_community, langchain_openai, langchain_core, langchain_text_splitters
  - faiss-cpu (or faiss-gpu)
  - python-dotenv

If you prefer, create a `requirements.txt` with pinned versions.

## Setup (Windows PowerShell)

Open PowerShell in the project root `D:\Confidential\Doxa-Langchain` and run:

```powershell
# create venv (if you don't have one already)
python -m venv .venv
# activate
.\.venv\Scripts\Activate.ps1
# install required packages (adjust versions as needed)
python -m pip install --upgrade pip
pip install langchain langchain_community langchain_openai langchain_core langchain_text_splitters python-dotenv faiss-cpu
```

## Environment

Create a `.env` file in the project root with your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

The code uses `python-dotenv` (the project already calls `load_dotenv()`), so environment variables from `.env` will be loaded.

## Running the examples

Run the PDF loader module (safe as a module):

```powershell
py -m modules.process_pdf
```

Run the QA pipeline (this creates embeddings, FAISS index, and runs a sample question):

```powershell
py -m modules.qa_chain
```

If you prefer using the venv python directly:

```powershell
& .\.venv\Scripts\python.exe -m modules.qa_chain
```

## Troubleshooting

- ValueError: File path is not valid
  - Ensure PDFs are in the `docs/` folder and `modules/process_pdf.py` resolves the path correctly.
- Module import errors (e.g., `No module named 'langchain.chains'`)
  - LangChain has many package reorganizations. If an import fails, inspect available modules in the venv or check the package version.
  - Example to check versions:
    ```powershell
    python -c "import langchain; print(langchain.__version__)"
    ```
- OpenAI auth errors
  - Confirm `OPENAI_API_KEY` is set in `.env` or environment.
- FAISS import errors
  - Install `faiss-cpu` or `faiss-gpu`:
    ```powershell
    pip install faiss-cpu
    ```
