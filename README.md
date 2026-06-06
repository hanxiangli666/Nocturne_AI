# Nocturne AI

An applied AI learning lab for building practical LLM workflows: RAG, LangChain LCEL chains, Streamlit assistants, memory-aware chat, data analysis outputs, and small agent experiments.

## Why This Exists

This repository is not a single polished product. It is a structured practice space for turning LLM concepts into runnable applications. The strongest evidence here is the progression from API calls and prompt experiments into RAG, memory, streaming UI, and educational assistant prototypes.

## Key Projects

### 1. Product RAG with history-aware retrieval

File: `RAG.py`

Builds a local retrieval-augmented generation chain over `data/ProductFile.txt`.

Technical details:

- `TextLoader` for local document loading
- `RecursiveCharacterTextSplitter` for chunking
- `HuggingFaceEmbeddings` with `all-MiniLM-L6-v2`
- FAISS vector store
- LangChain LCEL retrieval chain
- `create_history_aware_retriever` for follow-up question rewriting
- `create_stuff_documents_chain` for answer generation
- manual chat history with `HumanMessage` and `AIMessage`
- OpenAI-compatible chat client using DeepSeek endpoint

### 2. Omni AI Learning Assistant

Path: `Omni-AI-Learning-Assistant/`

A Streamlit AI tutor with configurable subjects, teaching style, memory, and streaming responses.

Features:

- Subjects: Computer Science, Mathematics, Physics, Biology, Literature, History
- Teaching styles: Concise, Detailed, Socratic
- Streamlit chat interface
- `ChatMessageHistory` stored in `st.session_state`
- `RunnableWithMessageHistory` for conversation memory
- temperature slider for model behavior control
- LaTeX-friendly prompt rules for STEM explanations
- OpenAI-compatible API support

### 3. Data analysis artifacts

Paths:

- `artifacts/`
- `outputTable/`
- `14/`
- `15/`

Contains generated charts and CSV summaries for traffic, monthly funnel, revenue trends, and category completion rate.

### 4. Small AI engineering exercises

Examples:

- `agent.fibonacci_caluculator.py`
- `memory.py`
- `partial_variables.py`
- `Translation.py`
- `Creativity.py`
- `Max_tokens.py`

These files document API parameter practice, memory concepts, tool-style agents, and prompt behavior experiments.

## Tech Stack

- Python
- Streamlit
- LangChain / LCEL
- FAISS
- HuggingFace sentence-transformer embeddings
- OpenAI-compatible chat APIs
- DeepSeek-compatible endpoint
- pandas / chart artifacts

## Run The Learning Assistant

```powershell
cd Omni-AI-Learning-Assistant
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python -m streamlit run app.py
```

Set your API key in `.env` or Streamlit secrets.

## What This Repository Demonstrates

- Ability to move beyond API calls into RAG and memory-aware workflows.
- Understanding of retrieval, chunking, embeddings, vector search, and prompt orchestration.
- Product sense for educational AI assistants, not only notebook experiments.
- Practical Streamlit UI work with streaming and session state.

## Next Improvements

- Split each app into its own cleaner subproject.
- Add screenshots and short demo GIFs.
- Add tests for prompt assembly and retriever behavior.
- Replace duplicated bilingual README fragments with one evidence-first project narrative.
