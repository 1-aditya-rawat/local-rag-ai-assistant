PROMPT_TEMPLATE = """
You are a helpful AI assistant.

Answer ONLY from provided context.

If information is missing, say:
"I could not find this in uploaded documents."

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer:
"""