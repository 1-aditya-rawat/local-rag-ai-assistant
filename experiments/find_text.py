from database import collection

data = collection.get()

for i, doc in enumerate(data["documents"]):

    if "f-string" in doc.lower():
        print(f"\nFOUND IN CHUNK {i}")
        print(doc[:1000])

# data = collection.get()

count = 0

for doc in data["documents"]:
    if "f-string" in doc.lower():
        count += 1
        print(doc[:500])

print("\nTotal Matches:", count)