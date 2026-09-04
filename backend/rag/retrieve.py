from rag.vectorstore import get_vectorstore


def retrieve_documents(query: str, k: int = 4):
    """
    Retrieve the most relevant document chunks
    for a given user query.
    """

    vectorstore = get_vectorstore()

    documents = vectorstore.similarity_search(
        query,
        k=k,
    )

    return documents


if __name__ == "__main__":
    query = input("Ask a question: ")

    documents = retrieve_documents(query)

    print(f"\nRetrieved {len(documents)} documents:\n")

    for i, document in enumerate(documents, start=1):
        print("=" * 80)
        print(f"RESULT {i}")
        print("=" * 80)

        print(document.page_content)

        print("\nMetadata:")
        print(document.metadata)


        