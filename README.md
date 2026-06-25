# 📚 Local RAG AI Assistant

A conversational Retrieval-Augmented Generation (RAG) assistant built using Streamlit, Ollama, and ChromaDB.

The application allows users to upload PDF documents, ask questions, retrieve relevant context, and generate answers with source attribution.

---

## Features

✅ PDF Upload

✅ Text Chunking

✅ Embedding Generation

✅ ChromaDB Vector Storage

✅ Conversational Memory

✅ Query Rewriting

✅ Multi-PDF Search

✅ Retrieval Thresholding

✅ Hallucination Prevention

✅ Source Attribution

✅ Retrieval Metrics Dashboard

---

## Tech Stack

- Python
- Streamlit
- Ollama
- ChromaDB
- PyPDF2

---

## Project Structure

```text
local-rag-ai-assistant/
│
├── app.py
├── config.py
├── services/
├── utils/
├── data/
├── evaluation/
├── experiments/
```

---

## Architecture

PDF
↓
Text Extraction
↓
Chunking
↓
Embeddings
↓
ChromaDB

Question
↓
Query Rewriting
↓
Retriever
↓
Threshold Check
↓
Phi3
↓
Answer + Sources

---

## Installation

```bash
git clone <repository-url>

cd local-rag-ai-assistant

pip install -r requirements.txt
```

---

## Run

```bash
streamlit run app.py
```

---

## Screenshots

(Add screenshots here)

---

## Future Improvements

- Hybrid Search
- Re-ranking
- Web Search Integration
- Better Evaluation Metrics
- Cloud Deployment

---

## Resume Bullet

Developed a local RAG-based AI assistant using Ollama, ChromaDB, and Streamlit with conversational memory, metadata filtering, retrieval evaluation, source attribution, and hallucination prevention.