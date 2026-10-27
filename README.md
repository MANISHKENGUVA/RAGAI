# Narada chat widget and API prototype

This repository contains the embeddable Narada chat widget, example host
clients, and an early FastAPI backend foundation. It is a prototype: the
Python API does not yet implement document ingestion, retrieval, model
generation, streaming, authentication, or persistence.

## Widget and client examples

The Vue 2/Vite SDK is in [`Narada_SDK`](./Narada_SDK/README.md). Runnable
plain HTML, React, Vue, and Angular host examples are in
[`CLIENT_USER`](./CLIENT_USER/README.md).

Install the npm workspace, then build the SDK and host clients:

```sh
npm ci
npm run build:sdk
npm run build:clients
```

Run an example from the repository root with `npm run dev:html`,
`npm run dev:react`, `npm run dev:vue`, or `npm run dev:angular`.
The aggregate `npm run build` also invokes an integration-portal workspace
that is not present in this checkout, so it currently exits with an error
after building the SDK and clients.

## Python API foundation

Setup, configuration, current endpoint behavior, and tests are documented in
[`narada-rag-backend/README.md`](./narada-rag-backend/README.md). The API
provides health/readiness endpoints and validated errors. Its chat route
returns HTTP 501 until generation is implemented, and the widget's current
`{app_id, query}` SSE contract is not yet compatible with the backend's
prototype request model.
