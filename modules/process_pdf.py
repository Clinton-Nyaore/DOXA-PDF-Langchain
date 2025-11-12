import os
from langchain_community.document_loaders import PyPDFLoader

def pdf_processor(file):
    """Extract text from the uploaded PDF file."""
    pdf_loader = PyPDFLoader(file)
    documents = pdf_loader.load()
    return documents

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(base_dir, "docs", "clinton_profile.pdf")
    documents = pdf_processor(pdf_path)
    print(f"Loaded {len(documents)} documents from the PDF.")