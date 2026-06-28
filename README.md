# 🤖 AI RAG Chatbot

## 📌 Overview

AI RAG Chatbot is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF and DOCX documents and ask questions about their content. The chatbot retrieves relevant information from the uploaded documents using ChromaDB and generates accurate answers with Ollama (Llama 3.2).

---

## 🚀 Features

* 📄 Upload PDF and DOCX documents
* 🔍 Semantic search using ChromaDB
* 🤖 AI-powered question answering
* 🎤 Voice input (Speech Recognition)
* 🔊 Voice output (Text-to-Speech)
* 💬 Continuous voice conversation
* 📧 AI Email Integration
* 🗑 Delete uploaded documents
* 💾 Chat memory support

---

## 🛠 Tech Stack

### Backend

* Python
* FastAPI
* ChromaDB
* Sentence Transformers
* Ollama (Llama 3.2)

### Frontend

* HTML
* CSS
* JavaScript

---

## 📂 Project Structure

```
AI-RAG-CHATBOT/
│
├── backend/
│   ├── main.py
│   ├── rag.py
│   ├── vector_store.py
│   ├── embedding.py
│   ├── search.py
│   ├── llm.py
│   ├── email_service.py
│   └── ...
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/KoduruDeekshitha/AI-RAG-CHATBOT.git
```

Move into the project

```bash
cd AI-RAG-CHATBOT
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the backend

```bash
uvicorn backend.main:app --reload
```

Open the frontend in your browser.

---

## 📖 Usage

1. Upload a PDF or DOCX file.
2. Ask questions about the uploaded document.
3. Receive AI-generated answers.
4. Use voice input for hands-free interaction.
5. Listen to AI responses with voice output.
6. Send AI-generated emails.

---

## 🔮 Future Improvements

* 📞 AI Phone Calling
* 📱 SMS Integration
* 📅 Google Calendar Integration
* 🌐 Website Chat
* 🖼 OCR Support
* 🤖 AI Agent with Tool Calling

---

## 👩‍💻 Author

**Deekshitha Koduru**

GitHub: https://github.com/KoduruDeekshitha
