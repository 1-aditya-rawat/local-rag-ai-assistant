# evaluation_results.py

from database import search_chunks

questions = [
    "What is a string in Python?",
    "What does len() do?",
    "What are f-strings?"
]

print("\nQuestion | Retrieval")

for q in questions:

    docs, metadata = search_chunks(q)

    print(f"\n{q}")

    retrieved = input(
        "Relevant? (1=yes,0=no): "
    )

    print("Retrieval:", retrieved)