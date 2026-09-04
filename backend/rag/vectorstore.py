from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Persistent ChromaDB directory
CHROMA_DIR = BASE_DIR / "chroma_db"


# Embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


def get_vectorstore():
    """
    Return the persistent Chroma vector store.
    """

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )

    return vectorstore
