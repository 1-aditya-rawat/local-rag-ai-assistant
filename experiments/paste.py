# app.py
# import streamlit as st

# from pdf_reader import extract_text_from_pdf
# from utils import chunk_text
# from database import store_chunks,collection
# from rag import ask_question


# st.set_page_config(page_title="AI PDF Assistant")


# st.sidebar.title("Database Stats")

# total_docs = collection.count()

# st.sidebar.write(
#     f"Stored Chunks: {total_docs}"
# )

# existing = collection.get()

# files = set()

# for meta in existing["metadatas"]:
#     if meta:

#         files.add(
#             meta["source"]
#         )

# st.sidebar.write(
#     # f"Messages: {len(st.session_state.get('messages', []))}"
#     f"Files Stored:{len(files)}"
# )

# if st.sidebar.button("Clear Chat"):
#     st.session_state.messages = []
#     st.rerun()

# st.title("📚 AI PDF Assistant")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# st.sidebar.write(
#     f"Messages: {len(st.session_state.messages)}"
# )


# if "processed_file" not in st.session_state:
#     st.session_state.processed_file = None

# uploaded_file = st.file_uploader(
#     "Upload PDF",
#     type="pdf"
# )

# if uploaded_file:

#     st.success("PDF Uploaded Successfully")

#     # Extract text
#     text = extract_text_from_pdf(uploaded_file)

#     # Create chunks
#     chunks = chunk_text(text)

#     # Store only once
#     if st.session_state.processed_file != uploaded_file.name:

#         result = store_chunks(
#             chunks,
#             uploaded_file.name
#         )

#         st.session_state.processed_file = uploaded_file.name

#         st.sidebar.success(result)

#     else:
#         st.sidebar.info("File already processed")

#     st.sidebar.title("Uploaded File")
#     st.sidebar.write(uploaded_file.name)

#     # st.sidebar.success(result)

#     # ~~~~~~ File Selector ~~~~~~~
#     selected_file = st.selectbox(
#         "Choose PDF",
#         list(files)
#     )
 
# #~~~~~~~~ Question Section ~~~~~~~~~~
#     question = st.text_input(
#         "Ask question from PDF"
#     )
    
#     if question:
#         chat_history = ""

#         for msg in st.session_state.messages[-6:]:
#             chat_history += (
#                 f"{msg['role']}: "
#                 f"{msg['content']}\n"
#             )
        
#         st.session_state.messages.append({  
#             "role": "user",
#             "content": question
#         })

#         with st.spinner("Thinking..."):

#             answer, docs, metadata, distances = ask_question(
#             question,
#             chat_history
#         )


#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": answer
#         })

#         st.subheader("Answer")

#         st.write(answer)

#         st.subheader("Retrieved Sources")

#         for doc, meta, dist in zip(docs, metadata, distances    ):
#             print(meta)

#             if meta:
#                 with st.expander(f"📄 {meta['source']}"):
#                     st.write( f"Chunk ID: {meta.get('chunk_id', 'Unknown')}") 
#                     st.write( f"Distance: {dist}" )
#                     st.write(doc)
#             else:
#                 st.write("📄 Source: Unknown")

            

#             st.write("------")


# st.subheader("Chat History")

# for msg in st.session_state.messages:

#     st.write(
#         f"{msg['role']}: {msg['content']}"
#     )   

# rag.py

# import ollama

# from database import search_chunks
# from prompts import PROMPT_TEMPLATE


# def ask_question(question, chat_history):

# #~~~~~ Retrieve Docs ~~~~~
#     docs, metadata,distances = search_chunks(question, chat_history)
#     print(metadata)
# # Context from retrieved chunks
#     context = "\n".join(docs)

# #~~~~~ Chat History ~~~~~

#     # for msg in st.session_state.messages[-6:]:
#     #     chat_history += (
#     #         f"{msg['role']}: "
#     #         f"{msg['content']}\n"
#         # )

# # Updated prompt
#     prompt = PROMPT_TEMPLATE.format(
#         history=chat_history,
#         context=context,
#         question=question
#     )

#     response = ollama.chat(
#         model="phi3:mini",
#         messages=[{
#             "role":"user",
#             "content" : prompt 
#         }]

#     return (
#         response["message"]["content"],
#         docs,
#         metadata,
#         distances                   
#     )

# database.py
# import chromadb
# import ollama
# import uuid

# client = chromadb.PersistentClient(path="chroma_db")

# collection = client.get_or_create_collection(
#     name="pdf_collection"
# )

# # def store_chunks(chunks):

# #     print("TOTAL CHUNKS:",len(chunks))

# #     for chunk in chunks:

# #         embedding = ollama.embeddings(
# #             model="nomic-embed-text",
# #             prompt=chunk
# #         )["embedding"]

# #         collection.add(
# #             ids=[str(uuid.uuid4())],
# #             documents=[chunk],
# #             embeddings=[embedding]
# #         )
# #     print("Chunks stored successfully")


# def store_chunks(chunks, filename):

#     existing = collection.get()

#     sources = []

#     if existing["metadatas"]:
#         for meta in existing["metadatas"]:

#             if meta:
#                 sources.append(
#                     meta.get("source")
#                 )

#     if filename in sources:
#         return "File already exists"

#     print("TOTAL CHUNKS:", len(chunks))
#     print("\nFIRST CHUNK:")
#     print(chunks[0][:500])

#     for i, chunk in enumerate(chunks):

#         # embedding = model.encode(chunk).tolist()
#         embedding = ollama.embeddings(
#             model="nomic-embed-text",
#             prompt=chunk
#         )["embedding"]


#         collection.add(
#             ids=[f"{filename}_{i}_{uuid.uuid4()}"],
#             embeddings=[embedding],
#             documents=[chunk],
#             metadatas=[{
#                 "source": filename,
#                 "chunk_id": i
#             }]
#         )

#     return "Stored successfully"
    

# def search_chunks(query, chat_history):
#             # ~~~~~ Query Rewriting ~~~~~
#     QUERY_MAP = {
#     "ml": "machine learning",
#     "dl": "deep learning",
#     "rl": "reinforcement learning",
#     "ai": "artificial intelligence"
#     }

#     # query = query.lower()
#     query = query(
#         where = {"source": selected_file}
#     )
#     for short, full in QUERY_MAP.items():
#         query = query.replace(short, full)
    
#     FOLLOWUP_WORDS = [
#         "it",
#         "this",
#         "that",
#         "these",
#         "those",
#         "explain",
#         "simplify"
#     ]

#     if any(word in query.lower()
#        for word in FOLLOWUP_WORDS):
#         query = chat_history + " " + query  
    
#     print("\nFINAL QUERY:")
#     print(query)


#     query_emb = ollama.embeddings(
#         model="nomic-embed-text",
#         prompt=query
#     )["embedding"]

#     results = collection.query(
#         query_embeddings=[query_emb],
#         n_results=3,
#         where=  {"source": selected_file}
#     )
#     # print(results)
#     print("\n===== RETRIEVED TEST =====")
#     print("Question:",query)
    
#     # print("\nDocs")
#     # docs = results["documents"][0]

#     # metadata = results["metadatas"][0]

#     print("\nDistances:")
#     print(results["distances"][0])

#     for i,doc in enumerate(results["documents"][0],start=1):
#         print(f"\nDoc {i}")
#         print(doc[:300])

#     return (
#         results["documents"][0],
#         results["metadatas"][0],
#         results["distances"][0]
#     )
#     )



