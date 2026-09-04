from rag.retrieve import retrieve_documents
from rag.generator import generate_answer


def build_context(documents) -> str:
    """
    Convert retrieved documents into a single context string.
    """

    context_parts = []

    for i, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "Unknown")
        page = document.metadata.get("page_label", "Unknown")

        context_parts.append(
            f"[Source {i} | Page {page}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)


def ask_question(query: str, k: int = 4):
    """
    Run the complete RAG pipeline.
    """

    # Retrieve relevant chunks
    documents = retrieve_documents(query, k=k)

    # Build context
    context = build_context(documents)

    # Generate answer
    answer = generate_answer(
        query=query,
        context=context,
    )

    return {
        "answer": answer,
        "sources": documents,
    }


if __name__ == "__main__":
    query = input("Ask a question: ")

    result = ask_question(query)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)

    print(result["answer"])

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for i, document in enumerate(result["sources"], start=1):
        print(f"\nSource {i}")
        print(f"Page: {document.metadata.get('page_label', 'Unknown')}")
        print("-" * 80)
        print(document.page_content)