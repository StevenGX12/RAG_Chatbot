# 🧠 Technical Interview RAG Chatbot

This is a full-stack **Retrieval-Augmented Generation (RAG)** chatbot system designed to help users prepare for software engineering technical interviews. It combines local document retrieval with a large language model (LLM) to answer questions based on custom educational content like PDFs, slides, spreadsheets, and more.

![Chatbot Screenshot](assets/screenshot.png)

---

## 🚀 Features

- Multimodal document ingestion: PDF, DOCX, PPTX, CSV
- Local embedding using `sentence-transformers`
- Vector store using **ChromaDB**
- Conversational retrieval with contextual prompt building
- FastAPI backend API
- Streamlit frontend with modern chat UI
- Modular Python architecture (easy to extend)

---

## ⚙️ Setup Guide

Follow the steps below to install dependencies, process documents, and launch the chatbot:

### 1. Clone the repository

```bash
git clone https://github.com/StevenGX12/RAG_Chatbot.git
cd technical-interview-rag
```

### 2. Set up the virtual environment

```bash
python -m venv myenv
source myenv/bin/activate       # On Windows: myenv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama (if using a local model)

Ensure you've installed Ollama and pulled a model:

```bash
ollama run gemma3
```

### 5. Add documents to the corpus

Place all your learning materials under the folder:

```bash
./corpus/
```
Supported formats: .pdf, .docx, .pptx, .csv

### 6. Run the document processing pipeline

```bash
python -m src.scripts.update_db
```

This will:
- Parse and chunk new documents
- Generate embeddings for unembedded chunks
- Add them to the ChromaDB vector store

### Start the FastAPI backend

```bash
uvicorn src.app_backend:app --reload
```

Runs on: http://localhost:8000

### Launch the Streamlit frontend

In a separate terminal: 

```bash
streamlit run src.app_frontend.py
```

### File Structure

```bash
src/
├── scripts/                  # Utilities: update_db, backfill
├── app_backend.py           # FastAPI server
├── app_frontend.py          # Streamlit chat UI
├── data_loader.py           # Corpus parser and processor
├── embedder.py              # Embeds document chunks
├── retriever.py             # Query-time document retrieval
├── vector_store.py          # ChromaDB logic
├── generator.py             # Prompt building and LLM calls
processed_corpus/            # Output: chunks and embeddings
corpus/                      # Input: source documents
assets/                      # UI assets like screenshots
```
