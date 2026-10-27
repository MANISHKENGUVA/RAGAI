# Narada Python API foundation

This directory contains an early FastAPI API foundation. It is not yet a RAG
backend: document ingestion, retrieval, model calls, streaming, authentication,
and persistence are not implemented. `POST /api/chat` therefore returns
`501 chat_not_implemented`; it does not return a fabricated answer.

## Setup

Python 3.12 was used for the recorded verification. From this directory,
create and activate a virtual environment, then install the locked dependencies
for the API foundation:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-foundation.lock
cp .env.example .env
```

`requirements-foundation.lock` pins the API/test/server dependency set. The
broader `requirements.txt` also lists packages intended for later RAG phases;
it is lower-bounded and not yet locked. The current API foundation does not
initialize Qdrant, download an embedding model, or require provider
credentials.

`APP_NAME` is the only setting currently read by the API. The Qdrant,
embedding, document-directory, and CORS values in `.env.example` are
placeholders for planned work and are not wired into the application. Keep
secrets out of `.env.example` and source control.

## Run

From this directory:

```sh
uvicorn app.main:app --reload
```

- `GET /health` reports that the process is running.
- `GET /ready` reports that this API foundation is ready; it does not check
  external model or vector-store dependencies.
- `POST /api/chat` validates the current prototype request shape
  (`company_id`, `question`, optional `top_k`) and returns a structured 501
  error for valid requests until generation is implemented.

Errors use `{"error":{"code","message","request_id","details"}}`; `details`
is present for validation failures. Unexpected errors are logged with the
request ID and exception type, while internal exception messages are not
returned to clients. `X-Request-ID` is included on normal and handled
validation responses.

The embeddable widget currently posts a different body (`app_id`, `query`)
and expects Server-Sent Events. It is not compatible with this API yet. No
authentication or tenant authorization is implemented; a client-supplied
workspace identifier must not be treated as an authorization decision.

## Tests

Run the unit/API tests from this directory:

```sh
python -m unittest discover -s tests -v
```

Tests use HTTPX's in-process ASGI transport and do not call paid model
providers or external vector services.
