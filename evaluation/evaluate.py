from database import search_chunks

with open("evaluation_questions.txt", "r") as f:
    questions = f.readlines()

print("\n" + "="*80)
print("RAG EVALUATION")
print("="*80)

for q in questions:

    q = q.strip()

    if not q:
        continue

    print("\n" + "="*50)
    print("QUESTION:", q)

    docs, metadata = search_chunks(q)

    print("\nTOP RETRIEVED CHUNK:")

    if docs:
        print(docs[0][:400])

    print("\nSOURCE:")

    if metadata and metadata[0]:
        print(metadata[0].get("source"))