📊 Help Assistant Chatbot

An intelligent AI-powered assistant that answers user queries using document knowledge + real-time web search. The system dynamically decides whether local knowledge is sufficient or if external information is required.

🚀 Project Overview

This chatbot is built using a 3-layer architecture:

Frontend: Streamlit-based chat UI (dark theme, real-time interaction)
Backend: FastAPI handling document upload and query processing
Data Layer: Chroma Vector DB + Groq LLM + SerpAPI Web Search

👉 Repository:
Help Assistant GitHub Repo

🧠 Key Features

📄 1. Document-Based Q&A (RAG)
Upload PDF documents
Automatic text chunking (500 chars, 100 overlap)
Embedding generation using HuggingFace (embeddinggemma-300m)
Stored in ChromaDB (SQLite persistence)

🔍 2. Smart Query Processing
Extracts structured metadata:
Intent
Priority
Sentiment
Issue Type
Retrieves Top-3 relevant document chunks
Uses LLM to generate contextual answers

🤖 3. Autonomous Tool Calling Agent
Model: Groq llama-3.1-8b-instant
Tool: Web Search (SerpAPI)

💡 Intelligent behavior:

Uses documents first
Calls web search ONLY if information is insufficient
Avoids unnecessary API calls

🌐 4. Real-Time Web Search Integration
Fetches clean, summarized results
Sanitizes output to prevent token overflow
Ensures accurate and up-to-date answers

🏗️ System Architecture
User Query
   ↓
Frontend (Streamlit UI)
   ↓
Backend (FastAPI)
   ↓
Query Analysis (Intent + Sentiment)
   ↓
Vector Search (Chroma DB)
   ↓
LLM Decision Layer
   ├── Use Docs → Generate Answer
   └── Call Web Search → Merge + Answer
   ↓
Final Response to User

⚙️ API Endpoints
📤 /upload_docs
Upload PDF files
Automatically processes and stores embeddings
💬 /user_query
Accepts user query
Performs:
Query analysis
Vector retrieval
LLM reasoning
Optional web search


🧪 Testing Result
Query:
"What is capital of France?"
Outcome:
LLM identified insufficient local docs
Called web_search tool automatically
Returned clean and correct response

✅ No tool traces leaked
✅ Response was structured and natural

📦 Tech Stack
Frontend: Streamlit
Backend: FastAPI
LLM: Groq (llama-3.1-8b-instant)
Embeddings: HuggingFace (embeddinggemma-300m)
Vector DB: Chroma (SQLite)
Search Tool: SerpAPI

🔑 Core Design Principle
"Let the LLM decide when external knowledge is needed."

This avoids:
Over-reliance on web APIs
Hallucinations from missing context
Token inefficiency

📌 Future Improvements
Add retrieval scoring & reranking
Support multi-document reasoning
Implement chat memory (conversation context)
Add streaming responses
Improve UI/UX with typing indicators & history

🛠️ Setup Instructions
# Clone the repository
git clone https://github.com/shubhamacharya77/Help_assistant.git

# Navigate to project folder
cd Help_assistant

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload

# Run frontend
streamlit run app.py

📄 License
This project is open-source and available under the MIT License.

✨ Summary
This project demonstrates a production-style AI assistant combining:
Retrieval-Augmented Generation (RAG)
Tool-calling agents
Real-time web search
