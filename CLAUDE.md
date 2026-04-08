# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Project

The primary way to run this project is via Docker Compose:

```bash
docker-compose up -d --build
```

To run the FastAPI app locally (without Docker):

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Setup

All configuration comes from a `.env` file. Required variables:

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL_NAME` | e.g. `gpt-4o` |
| `OPENAI_MODEL_TEMPERATURE` | Float, e.g. `0` |
| `AI_CONTEXTUALIZE_PROMPT` | System prompt to reformulate questions given chat history |
| `AI_SYSTEM_PROMPT` | Main RAG system prompt — must include `{context}` placeholder |
| `VECTOR_STORE_PATH` | Path to persist ChromaDB data (e.g. `/app/vectorstore`) |
| `RAG_FILES_DIR` | Directory to watch for new PDFs/TXTs (e.g. `/app/rag_files`) |
| `EVOLUTION_API_URL` | Base URL for Evolution API (WhatsApp gateway) |
| `EVOLUTION_INSTANCE_NAME` | Evolution API instance name |
| `AUTHENTICATION_API_KEY` | Evolution API key |
| `CACHE_REDIS_URI` | Redis connection string (e.g. `redis://redis:6379`) |
| `BUFFER_KEY_SUFIX` | Suffix appended to `chat_id` for Redis buffer keys |
| `DEBOUNCE_SECONDS` | Seconds to wait after last message before processing |
| `BUFFER_TTL` | TTL (seconds) for Redis buffer keys |

## Architecture

The request flow through the system is:

```
WhatsApp user → Evolution API (webhook POST /webhook) → message_buffer.py → chains.py → Evolution API (send reply)
```

### Key components

**[app.py](app.py)** — FastAPI entrypoint. Single `POST /webhook` route. Filters out group messages (`@g.us`) and delegates to `buffer_message`.

**[message_buffer.py](message_buffer.py)** — Implements debouncing. Each incoming message is `RPUSH`-ed to a Redis list keyed by `{chat_id}{BUFFER_KEY_SUFIX}`. A per-user asyncio task waits `DEBOUNCE_SECONDS`; if a new message arrives it cancels and restarts the timer. After silence, all buffered messages are joined and sent together to the RAG chain.

**[chains.py](chains.py)** — Builds the LangChain RAG pipeline: `history_aware_retriever` (reformulates questions using chat history) → `stuff_documents_chain` (answers from retrieved context) → wrapped in `RunnableWithMessageHistory` using Redis-backed session history.

**[vectorstore.py](vectorstore.py)** — On each startup, scans `RAG_FILES_DIR` for new `.pdf`/`.txt` files, chunks them (1000 chars, 200 overlap), embeds via OpenAI Embeddings, and stores in ChromaDB at `VECTOR_STORE_PATH`. Processed files are moved to `RAG_FILES_DIR/processed/`.

**[memory.py](memory.py)** — Provides `RedisChatMessageHistory` per `session_id` (which equals `chat_id`) for conversation persistence.

**[prompts.py](prompts.py)** — Defines two LangChain prompts loaded from `.env`: `contextualize_prompt` (rewrites user input given history) and `qa_prompt` (the main answer-generation prompt with `{context}` injected).

### Infrastructure (docker-compose.yml)

- `bot` (port 8000): FastAPI app
- `evolution-api` (port 8080): WhatsApp gateway, requires `postgres` and `redis`
- `redis` (port 6379): message buffer + chat history
- `postgres` (port 5432): used internally by Evolution API

### Adding knowledge to the RAG

Drop `.pdf` or `.txt` files into the `rag_files/` directory and restart the `bot` container. Files are automatically ingested on startup and moved to `rag_files/processed/`.
