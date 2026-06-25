from database import collection
from database import search_chunks




    # while True:

    #     query = input("\nQuestion (type exit): ")

    #     if query.lower() == "exit":
    #         break

    #     docs, metadata = search_chunks(query)

    #     print("\nRESULTS\n")

    #     for i, (doc, meta) in enumerate(zip(docs, metadata), start=1):

    #         print(f"\nResult {i}")

    #         print("Metadata:")
    #         print(meta)

    #         print("\nText:")
    #         print(doc[:300])

    #         print("\n" + "=" * 50)

data = collection.get()

for i, doc in enumerate(data["documents"]):

    if "f-string" in doc.lower():
        print(f"\nFOUND IN CHUNK {i}")
        print(doc[:1000])
print("Total Chunks:")
print(collection.count())

print("\nSources Returned:")

for meta in metadata:
    print(meta["source"])


# docs, metadata = search_chunks(
#     "What is Machine Learning?"
# )

# print(metadata)
# # print(docs)
# print(type(metadata))

# for doc, meta in zip(docs, metadata):
#     print(meta)
#     print(type(meta))

# existing = collection.get()

# print("FILES IN DATABASE:")

# files = set(
#     meta["source"]
#     for meta in existing["metadatas"]
#     if meta
# )

# print(files)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# data = collection.get()

# print("TOTAL DOCS:", len(data["documents"]))

# for i, doc in enumerate(data["documents"][:5]):
#     print(f"\n----- DOC {i} -----")
#     print(doc[:500])