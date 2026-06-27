import streamlit as st

from services.pdf_reader import extract_text_from_pdf
from utils.chunking import chunk_text
from services.database import store_chunks,collection
from services.rag import ask_question
from config import DISTANCE_GREEN,DISTANCE_YELLOW,DEFAULT_THRESHOLD

#~~~~~~~ Retrieval Stats ~~~~~~~
if "retrieval_stats" not in st.session_state:
    st.session_state.retrieval_stats = []

if "failed_queries" not in st.session_state:
    st.session_state.failed_queries = 0

if "successful_queries" not in st.session_state:
    st.session_state.successful_queries = 0

#~~~~~~~~~~~~~~~ Export Storage ~~~~~~~~~~~~~~~~~~~
if "chat_exports" not in st.session_state:
    st.session_state.chat_exports = []

st.set_page_config(page_title="AI PDF Assistant")

st.sidebar.title("Database Stats")

total_docs = collection.count()

st.sidebar.write(
    f"Stored Chunks: {total_docs}"
)
#~~~~~~~~ Existing files ~~~~~~~~~~
existing = collection.get()

files = set()

for meta in existing.get("metadatas", []):
    if meta:
        files.add(
            meta["source"]
        )

#~~~~~~~~~ File Selector ~~~~~~~~~
file_list = sorted(list(files))

selected_file = None

if not file_list:
    st.info("Upload a PDF to begin.")

else:
    selected_file = st.selectbox(
        "Choose PDF",
        file_list
    )

#~~~~~~~~~~~           ~~~~~~~~~~~
st.sidebar.write(
    # f"Messages: {len(st.session_state.get('messages', []))}"
    f"Files Stored:{len(files)}"
)

# ~~~~~~~~~~~~ Clear Chat Button ~~~~~~~~~~~~~~~~~~
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ~~~~~~~~~~~ Chat Export Button ~~~~~~~~~~~~~
# if st.sidebar.button("Export Chat"):

#     chat_text = ""

#     for msg in st.session_state.messages:
#         chat_text += (
#             f"{msg['role']}: "
#             f"{msg['content']}\n\n"
#         )

#     with open("data/chat.txt", "w", encoding="utf-8") as f:
#         f.write(chat_text)

#     st.sidebar.success("Chat exported!")

if st.sidebar.button("Export Chat"):

    export_text = ""

    for chat in st.session_state.chat_exports:

        export_text += (
            f"Question: {chat['question']}\n\n"
            f"Answer:\n{chat['answer']}\n\n"
            f"Source: {chat['source']}\n"
            f"Distance: {chat['distance']:.2f}\n"
            "-----------------------------\n\n"
        )

    with open(
        "data/chat_export.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(export_text)

    st.sidebar.success("Chat exported!")

# ~~~~~~~~~~~~~~~~~ Sidebar Dashboard ~~~~~~~~~~~~~~~~~~~~~~

st.title("📚 AI PDF Assistant")

search_all = st.sidebar.checkbox(
    "Search All PDFs"
)

selected_source = None if search_all else selected_file

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.write(
    f"Messages: {len(st.session_state.messages)}"
)

st.sidebar.subheader("Query Stats")

st.sidebar.write(
    f"Successful: {st.session_state.successful_queries}"
)

st.sidebar.write(
    f"Failed: {st.session_state.failed_queries}"
)
# ~~~~~~~~~~~~~~~  Threshold Configure ~~~~~~~~~~~~~~
threshold = st.sidebar.slider(
    "Retrieval Threshold",
    200,
    600,
    DEFAULT_THRESHOLD
)
#~~~~~~~~~~~~~~~~~ Success Rate  ~~~~~~~~~~~~~~~~~~~~~~~~ 
total_queries = (
    st.session_state.successful_queries +
    st.session_state.failed_queries
)

if total_queries > 0:

    success_rate = (
        st.session_state.successful_queries
        / total_queries
    ) * 100

    st.sidebar.write(
        f"Success Rate: {success_rate:.1f}%"
    )
# ~~~~~~ Sidebar Metrics ~~~~~~
stats = st.session_state.retrieval_stats

if stats:

    distances_only = [
        s["distance"]
        for s in stats
    ]

    avg_distance = (
        sum(distances_only)
        / len(distances_only)
    )

    st.sidebar.subheader(
        "Retrieval Metrics"
    )

    st.sidebar.write(
        f"Average: {avg_distance:.2f}"
    )

    st.sidebar.write(
        f"Best: {min(distances_only)}"
    )

    st.sidebar.write(
        f"Worst: {max(distances_only)}"
    )


if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)


if uploaded_file:

    st.success("PDF Uploaded Successfully")

    # Extract text
    text = extract_text_from_pdf(uploaded_file)

    # Create chunks
    chunks = chunk_text(text)

    # Store only once
    if st.session_state.processed_file != uploaded_file.name:

        result = store_chunks(
            chunks,
            uploaded_file.name
        )

        st.session_state.processed_file = uploaded_file.name

        st.sidebar.success(result)

        st.rerun()

    else:
        st.sidebar.info("File already processed")

    st.sidebar.title("Uploaded File")
    st.sidebar.write(uploaded_file.name)

    # st.sidebar.success(result)
 
#~~~~~~~~ Question Section ~~~~~~~~~~
question = st.text_input(
    "Ask question from PDF"
)
    
if question:
    if not file_list and not search_all:
        st.warning("Upload a PDF first.")
        st.stop()

    chat_history = ""

    for msg in st.session_state.messages[-6:]:
        chat_history += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )
        
    st.session_state.messages.append({  
        "role": "user",
        "content": question
    })

    with st.spinner("Thinking..."):
        answer, docs, metadata, distances, best_distance, source  = ask_question(
            question,
            chat_history,
            selected_source,
            threshold
        )
        if not docs:
            st.session_state.failed_queries += 1
        else:
            st.session_state.successful_queries += 1
                
# ~~~~~~~~~~~~~~ Retrieval Logging ~~~~~~~~~~~~~~~~~~~~~
        chunk_id = "Unknown"

        if metadata:
            chunk_id = metadata[0].get(
                "chunk_id",
                "Unknown"
            )

        log_text = (
            f"Question: {question}\n"
            f"Source: {source}\n"
            f"Chunk: {chunk_id}\n"
            f"Distance: {best_distance}\n"
            f"----------------------\n"
        )

        with open(
            "data/retrieval_logs.txt",
            "a",
            encoding="utf-8"
        ) as f:
            f.write(log_text)
        st.write("Log written!")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
# ~~~~~~~~~~~ Retrieval Stats ~~~~~~~~~~
    st.session_state.retrieval_stats.append({
        "question" : question,
        "distance" : best_distance,
        "source" : source
    })
# ~~~~~~~~~~~ Chat Exports ~~~~~~~~~~~~
    st.session_state.chat_exports.append({
    "question": question,
    "answer": answer,
    "source": source,
    "distance": best_distance
    })

    st.subheader("Answer")
    st.write(answer)

# ~~~~~~~~~~~ Colour coding ~~~~~~~~~~~~~~~
    if best_distance < DISTANCE_GREEN:
        st.success("🟢 Good Retrieval")

    elif best_distance < DISTANCE_YELLOW:
        st.warning("🟡 Medium Retrieval")

    else:
        st.error("🔴 Poor Retrieval")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    st.subheader("Retrieved Sources")

    for doc, meta, dist in zip(docs, metadata, distances    ):
        print(meta)
        if meta:
            with st.expander(f"📄 {meta['source']}"):
                st.write( f"Chunk ID: {meta.get('chunk_id', 'Unknown')}") 
                st.write( f"Distance: {dist}" )
                st.write(doc)
        else:
            st.write("📄 Source: Unknown")
        st.write("------")
st.subheader("Chat History")

for msg in st.session_state.messages:   

    st.write(
        f"{msg['role']}: {msg['content']}"
    )   