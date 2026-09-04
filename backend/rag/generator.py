from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0,
)


def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using only the retrieved document context.
    """

    prompt = f"""
You are an AI document assistant.

Answer the user's question using ONLY the information
provided in the document context.

Rules:
- Do not use outside knowledge.
- Do not make up information.
- If the answer cannot be found in the context,
  say that you could not find the answer in the document.
- Give a clear and concise answer.

Document context:
--------------------
{context}
--------------------

User question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content