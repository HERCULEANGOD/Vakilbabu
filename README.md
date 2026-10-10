# Babu by VakilBabu

A production-ready chatbot starter for VakilBabu, built with FastAPI and a vanilla HTML/CSS/JS frontend.

## Features

- Modern chat UI
- FastAPI backend with CORS enabled
- Modular structure: config, models, routes, services
- Environment-based configuration
- Logging and basic error handling
- Local FAQ retrieval over 38 product-workflow questions
- Interactive FAQ guide grouped by product area
- Private environment settings kept out of source control

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
│   ├── knowledge/
│   │   └── faqs.json
│   └── services/
│       ├── __init__.py
│       ├── chatbot_service.py
│       └── faq_retriever.py
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
- GET `/api/faqs`
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
- `knowledge/faqs.json`: product FAQ questions and approved workflow answers
- `services/faq_retriever.py`: local FAQ retrieval and question categorization

## FAQ knowledge base

The chatbot uses a local TF-IDF retrieval layer over the FAQ corpus in `backend/knowledge/faqs.json`. The corpus covers account access, cases, clients, reminders, AI assistant workflows, and profile management. The chat API returns a concise answer when it finds a relevant FAQ; unrelated or unsupported questions receive a clarification response.

The FAQ file contains product workflows only. Test credentials, Admin instructions, and Security/access-control test cases are intentionally excluded. Do not add real credentials, API keys, or other secrets to the FAQ corpus.

The frontend loads categorized example questions from `GET /api/faqs`; selecting a question submits it to `POST /api/chat`.

## LLM integration points

`backend/services/chatbot_service.py` orchestrates responses and currently uses the local FAQ retriever. A future LLM adapter can be added alongside it, while retaining retrieval-grounded answers and fallback behavior.

## Recommended next steps

- Add a vector database and semantic retrieval if the FAQ corpus grows substantially
- Add authentication for internal users
- Add audit logging and conversation history
- Add document ingestion and legal dataset search
- Add message streaming for better UX
