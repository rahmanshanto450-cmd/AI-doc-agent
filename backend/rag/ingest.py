from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.vectorstore import get_vectorstore


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def ingest_pdf(pdf_path: str):
    """
    Load a PDF, split it into chunks,
    and store the chunks in ChromaDB.
    """

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages.")

    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # Get vector store
    vectorstore = get_vectorstore()

    # Add chunks to ChromaDB
    vectorstore.add_documents(chunks)

    print("Documents successfully added to ChromaDB.")


if __name__ == "__main__":
    pdf_path = DATA_DIR / "test.pdf"

    ingest_pdf(str(pdf_path))