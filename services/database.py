import chromadb
import ollama
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="pdf_collection"
)

DISTANCE_THRESHOLD = 410

def store_chunks(chunks, filename):

    existing = collection.get()

    sources = []

    if existing.get("metadatas"):
        for meta in existing["metadatas"]:

            if meta:
                sources.append(
                    meta.get("source")
                )

    if filename in sources:
        return "File already exists"

    print("TOTAL CHUNKS:", len(chunks))
    print("\nFIRST CHUNK:")
    print(chunks[0][:500])

    for i, chunk in enumerate(chunks):

        # embedding = model.encode(chunk).tolist()
        embedding = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )["embedding"]


        collection.add(
            ids=[f"{filename}_{i}_{uuid.uuid4()}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{
                "source": filename,
                "chunk_id": i
            }]
        )

    return "Stored successfully"
    

def search_chunks(
    query, 
    chat_history,
    selected_file,
    threshold
):

           # ~~~~~ Query Rewriting ~~~~~
    QUERY_MAP = {
    "ml": "machine learning",
    "dl": "deep learning",
    "rl": "reinforcement learning",
    "ai": "artificial intelligence"
    }

    words = query.lower().split()

    query = " ".join(
        QUERY_MAP.get(word, word)
        for word in words
    )
    # print("Original:", question)
    # print("Rewritten:", query)
    
    # for short, full in QUERY_MAP.items():
    #     query = query.replace(short, full)

    #~~~~~~~~ Follow-up handling ~~~~~~~~~~
    FOLLOWUP_WORDS = [
        "it",
        "this",
        "that",
        "these",
        "those",
        "explain",
        "simplify"
    ]

    if any(
        word in query.lower()
       for word in FOLLOWUP_WORDS
    ):
        query = chat_history + " " + query  
    
    print("\nFINAL QUERY:")
    print(query)

#~~~~~~~~~~~ Enbedding ~~~~~~~~~~~
    query_emb = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )["embedding"]

#~~~~~~~~~~~~ Filtering ~~~~~~~~~~~~~
    if selected_file:

        results = collection.query(
            query_embeddings=[query_emb],
            n_results=3,
            where=  {"source": selected_file}
        )
    else:
        results = collection.query(
            query_embeddings=[query_emb],
            n_results=3
        )
    # print(results)
    print("\n===== RETRIEVED TEST =====")
    print("Question:",query)
    
    # print("\nDocs")
    # docs = results["documents"][0]

    # metadata = results["metadatas"][0]

    print("\nDistances:")       
    print(results["distances"][0])

    for i,doc in enumerate(results["documents"][0],start=1):
        print(f"\nDoc {i}")
        print(doc[:300])

#~~~~~~~~~~~~~ Extraction ~~~~~~~~~~~~~
    docs = results["documents"][0]
    metadata = results["metadatas"][0]
    distances = results["distances"][0]


      #~~~ Empty retrieval ~~~
    if not docs:
        return [], [], []

      # ~~~ THRESHOLD ~~~
    # if distances and min(distances) > threshold:
    #     print("No relevant chunks found")
    #     return [], [], []
      #~~~ Return ~~~
    else:  
        return (
            docs,
            metadata,
            distances
        )