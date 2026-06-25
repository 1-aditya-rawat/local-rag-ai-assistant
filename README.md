# 📚 AI PDF Assistant (Local RAG)

A local Retrieval-Augmented Generation (RAG) assistant built using Streamlit, Ollama, and ChromaDB.

The application allows users to upload PDF documents, ask questions, retrieve relevant context from the documents, and generate grounded answers with source attribution.

---

## 🚀 Features

* PDF Upload and Processing
* Automatic Text Chunking
* Embedding Generation
* ChromaDB Vector Database
* Conversational Memory
* Query Rewriting
* Multi-PDF Retrieval
* Retrieval Thresholding
* Hallucination Prevention
* Source Attribution
* Retrieval Metrics Dashboard
* Evaluation Pipeline

---

## 🛠 Tech Stack

| Technology | Purpose         |
| ---------- | --------------- |
| Python     | Backend         |
| Streamlit  | User Interface  |
| Ollama     | Local LLM       |
| ChromaDB   | Vector Database |
| PyPDF2     | PDF Extraction  |

---

## 📂 Project Structure

```text
ai-pdf-assistant/
│
├── app.py
├── config.py
├── services/
├── utils/
├── data/
├── evaluation/
├── experiments/
├── screenshots/
└── README.md
```

---

## 🏗 Architecture

```text
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
```

---

## ⚙ Installation

```bash
git clone https://github.com/1-aditya-rawat/ai-pdf-assistant.git

cd ai-pdf-assistant

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶ Running the Application

```bash
streamlit run app.py
```

---

## 📈 Retrieval Metrics

The application tracks:

* Average retrieval distance
* Best retrieval distance
* Worst retrieval distance
* Success rate
* Failed queries

---

## 🔮 Future Improvements

* Hybrid Search
* Re-ranking
* Cloud Deployment
* Web Search Integration
* Better Evaluation Metrics
* Multiple LLM Support

---

## 📝 Resume Description

Developed a local RAG-based AI assistant using Ollama, ChromaDB, and Streamlit with conversational memory, retrieval evaluation, source attribution, and hallucination prevention.

## Screenshots

### Upload Interface

![Upload](screenshots/Screenshot%20(480).png)

### Generated Answer

![Answer](screenshots/Screenshot%20(482).png)