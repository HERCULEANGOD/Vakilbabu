# Babu by VakilBabu

A production-ready chatbot starter for VakilBabu, built with FastAPI and a vanilla HTML/CSS/JS frontend.

## Features

- Modern chat UI
- FastAPI backend with CORS enabled
- Modular structure: config, models, routes, services
- Environment-based configuration
- Logging and basic error handling
- Placeholder chatbot engine for future LLM/RAG integration

## Project structure

```text
vakilbabu-chatbot/
├── .env
├── .env.example
├── requirements.txt
├── README.md
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── logging_config.py
│   │   └── settings.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py
│   └── services/
│       ├── __init__.py
│       └── chatbot_service.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── .gitignore
```

## Run locally

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Start the backend:

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

3. Open the app in a browser:

```text
http://127.0.0.1:8000/
```

## API

- GET `/health`
- POST `/api/chat`

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```

## Architecture

- `routes/`: HTTP endpoints and request handling
- `services/`: business logic and chatbot orchestration
- `models/`: request/response schemas
- `config/`: environment and logging configuration

## LLM integration points

The placeholder logic sits in `backend/services/chatbot_service.py`. Replace the mock response function with a call to an LLM or a retrieval pipeline using your legal corpus.

## Recommended next steps

- Add a real vector database / RAG layer
- Add authentication for internal users
- Add audit logging and conversation history
- Add document ingestion and legal dataset search
- Add message streaming for better UX
