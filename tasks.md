# Narada RAG/SKB — Implementation Tasks

## 1. Current Status and Scope

- **Current maturity:** Basic prototype. The working-tree Python API foundation now starts and passes its focused tests, but the chat endpoint intentionally returns HTTP 501. This is not a RAG implementation.
- **In scope:** Evidence-based repository audit; a reliable, testable Python API foundation; independently tracked chatbot UI improvements.
- **Out of scope for this iteration:** Document ingestion, embeddings, vector retrieval, generated answers, LangGraph orchestration, authentication, persistence, and deployment. UI improvements are independently in scope, but backend-dependent states must not be simulated.
- **Known integration gap:** The widget sends `app_id` and `query` to its configured API URL and expects SSE. The repository-baseline backend exposed `/chat`, expected `company_id` and `question`, and returned a fixed echo. The current working-tree rewrite changes the route to `/api/chat`, but still expects the backend request model and returns HTTP 501; neither version integrates with the widget.
- **Known blockers/decisions:** LLM provider (including whether xAI/Grok is required), Qdrant deployment, tenant identity/authorization, authentication, streaming event contract, persistence, and deployment requirements are not confirmed by working backend code or a decision record.

## 2. Repository Audit Evidence

| Capability/task | Evidence (paths/symbols/tests) | Current status | Gaps |
|---|---|---|---|
| Repository and Git state | Root tree; `git status --short`; `git ls-files` | COMPLETED — VERIFIED (audit) | At audit start, `narada-rag-backend/app/main.py` was modified and `tasks.md` was untracked. Preserve these existing changes; do not treat the tree as clean. |
| Python API | [`narada-rag-backend/app/main.py`](narada-rag-backend/app/main.py), `create_app`, `health`, `readiness`, `chat`; [`narada-rag-backend/tests/test_api.py`](narada-rag-backend/tests/test_api.py) | PARTIALLY COMPLETE | Health/readiness, request IDs, validation/HTTP/unexpected error shapes, and explicit 501 chat behavior are tested. No chat generation, RAG, CORS, or widget-compatible SSE contract exists. |
| Python request validation | [`narada-rag-backend/app/CHATREQUEST/index.py`](narada-rag-backend/app/CHATREQUEST/index.py), `ChatRequest` | PARTIALLY COMPLETE | Company ID/question are non-blank and bounded; `top_k` is constrained to 1–20. Model still expects `company_id`/`question`, not widget `{app_id, query}`. |
| Python RAG/development work | `narada-rag-backend/DEVELOPMENT_TEST_KNOW/`; [`narada-rag-backend/requirements.txt`](narada-rag-backend/requirements.txt) | NOT STARTED (production backend) | Experimental files and dependency declarations are not proof of wired ingestion, retrieval, embeddings, provider calls, Qdrant, or tests. Those scripts were not used as production code evidence. |
| Backend configuration | [`narada-rag-backend/app/config.py`](narada-rag-backend/app/config.py); [`requirements-foundation.lock`](narada-rag-backend/requirements-foundation.lock); [`.env.example`](narada-rag-backend/.env.example) | COMPLETED — VERIFIED (foundation) | `APP_NAME` is typed and validated; the foundation dependency lock installs in a clean Python 3.12 environment. Qdrant, embedding, document, and CORS values remain placeholders and unused. |
| Frontend widget/API client | [`Narada_SDK/src/components/ChatContainer.vue`](Narada_SDK/src/components/ChatContainer.vue), `sendMessage`, `readEventStream`; [`CLIENT_USER/README.md`](CLIENT_USER/README.md) | PARTIALLY COMPLETE / NEEDS VERIFICATION | Client posts `{app_id, query}` and reads SSE. HTTP errors now use client-safe messages rather than displaying raw response bodies, but backend integration and stream error/retry behavior are not verified. |
| UI components and styling | [`Narada_SDK/src/components/ChatContainer.vue`](Narada_SDK/src/components/ChatContainer.vue), [`ChatHeader.vue`](Narada_SDK/src/components/ChatHeader.vue), [`MessageList.vue`](Narada_SDK/src/components/MessageList.vue), [`ChatWidget.scss`](Narada_SDK/dynamic-scss-theme/src/components/ChatWidget.scss) | PARTIALLY COMPLETE | Widget theme tokens now respond to palette/light-dark props; header is restrained; scroll-follow stops when the user reads older messages; suggestion copy no longer implies indexed workspace content. Sass build passes. No browser/screenshot, keyboard-only, contrast, or responsive visual verification; answer content is still plain text and there are no citations, retry button, stop-generation, offline, or abstention state. |
| UI/API documentation | [`CLIENT_USER/README.md`](CLIENT_USER/README.md); [`Narada_SDK/README.md`](Narada_SDK/README.md) | PARTIALLY COMPLETE | Client README describes the request and SSE expectation. SDK README documents the SCSS theme rather than a complete widget event/API contract. No real source metadata/citation schema is documented. |
| Automated tests | [`narada-rag-backend/tests/test_api.py`](narada-rag-backend/tests/test_api.py); `npm run test:platform` | PARTIALLY COMPLETE | Eight Python tests pass, including from a clean locked environment. The existing Node script exits 0 but discovers **0 tests**. |
| Build and CI | Root [`package.json`](package.json); `.github/workflows/` absent | PARTIALLY COMPLETE / NEEDS VERIFICATION | SDK and four host-client builds passed in `npm run build`; the overall command then failed because the `narada-integration-portal` workspace is absent. No CI workflow or Python lint/type check was found. |
| Dependencies/runtime | [`narada-rag-backend/requirements.txt`](narada-rag-backend/requirements.txt); [`requirements-foundation.lock`](narada-rag-backend/requirements-foundation.lock); local Python 3.12.3 | PARTIALLY COMPLETE | The API foundation has a clean-installable, exact-version lock. The broader future RAG requirements remain lower-bounded, uninstalled, and unvalidated. |

## 3. Completed — Verified

- Repository, existing task record/docs, tracked and working-tree backend state, widget components/styles, dependency manifests, test inventory, and CI inventory were audited.
- Backend Phase 1 is completed and verified for the API foundation: the exact-version lock installs into a clean environment; all eight API/configuration tests pass without model credentials; live Uvicorn health/readiness checks return 200. This does not complete any RAG feature.
- `npm run test:platform` exits 0 but discovers **0 tests**; this is not evidence of application behavior.
- SDK and host clients build successfully after `npm ci`. The full `npm run build` is still blocked at the missing integration-portal workspace.

## 4. Partially Complete

- **Python API foundation:** Configuration, request validation, health/readiness, request IDs, consistent error responses, a pinned foundation lock, and setup/test documentation are implemented and verified. Chat remains intentionally unimplemented (501); the broader planned RAG requirements are still unpinned and unvalidated.
- **Embeddable widget:** Vue components, streaming fetch/parser, theme styles, and host examples exist. Theme switching, safe HTTP error messages, and follow-scroll behavior were improved; backend integration and browser/accessibility/responsive visual behavior remain unverified.

## 5. Not Started

- Production document ingestion, safe parsing/chunking, idempotency, and vector writes.
- Embedding/retrieval adapter, relevance policy, grounded answer generation, citations, abstention, and prompt-injection evaluation.
- LangGraph workflow and graph persistence/checkpointing.
- Production API streaming contract and frontend integration against a real backend.
- Authentication/authorization, tenant isolation, rate/token limits, retention/deletion, observability, deployment/runbook, and release evaluation.
- Completion of the premium UI redesign and verified interaction/accessibility/regression testing.

## 6. Blocked / Needs Decision

| Decision/blocker | Impact | Required resolution |
|---|---|---|
| LLM provider; confirm or reject xAI/Grok | Cannot implement generation or provider-specific streaming safely. | Product decision and credentials through deployment secret management (never source control). |
| Qdrant local vs hosted deployment | Determines persistence, readiness checks, and integration test strategy. | Choose deployment/lifecycle and provide non-production test strategy. |
| Tenant/workspace identity and auth model | `app_id` from a browser request must not be trusted as authorization. | Define authenticated identity and server-side tenant mapping before data access. |
| SSE event schema and terminal/error semantics | Existing widget accepts several token-like fields but has no single strict contract; backend sends no SSE. | Confirm a versioned event schema and API route before implementation. |
| Conversation/document persistence and retention | Determines history, deletion, and privacy behavior. | Define whether persistence is required and its retention/deletion policy. |
| Allowed deployed client origins | CORS examples list localhost values only. | Supply deployment origins before configuring production CORS. |
| Reproducible dependencies and complete workspace build | Python requirements are not locked; root build also references an absent integration-portal workspace, and the existing Node test script discovers zero tests. | Add a Python lock and resolve the portal/build/test inventory gaps without claiming unverified work. |

## 7. Phased Roadmap

### Backend Phase 1 — Reliable Python foundation
- **Objective:** Typed validated configuration, a predictable FastAPI health/readiness surface, request/response validation, and consistent errors.
- **Tasks:** Replace print-time/demo behavior; add explicit settings and API models; define documented error semantics; add automated tests; document exact setup/test commands.
- **Dependencies:** No provider or vector DB decision required for a dependency-free readiness check. Do not claim a functioning chat/RAG endpoint.
- **Acceptance criteria:** Reproducible dependencies; validated settings; app startup; health/readiness behavior; tested API validation/error behavior; tests work without model credentials; README commands pass.
- **Verification:** `python -m unittest discover -s tests -v` and the documented app startup/health check.
- **Status:** COMPLETED — VERIFIED for the API foundation only. The foundation lock installs cleanly and the setup, tests, server startup, and health/readiness checks pass. The broader RAG dependency list is explicitly future-phase work.

### Backend Phase 2 — Document ingestion
- **Objective:** Validate, parse, normalize, chunk, identify, and safely store the explicitly selected document types.
- **Tasks:** Select supported formats; size/type/parser validation; stable IDs and metadata; idempotent replacement/deletion; isolated vector integration tests.
- **Dependencies:** Phase 1; storage and document-type decisions.
- **Acceptance criteria:** Unit tests for parsing/chunking/metadata/failures; isolated vector write/retrieval tests; documented re-ingestion behavior.
- **Status:** NOT STARTED.

### Backend Phase 3 — Retrieval and grounded RAG
- **Objective:** Retrieve relevant scoped evidence and generate grounded answers or abstentions.
- **Tasks:** Embedding/vector adapter; server-enforced scope filters; sufficiency policy; untrusted-context prompt construction; citation mapping; deterministic failures.
- **Dependencies:** Phase 1; Phase 2; provider, tenant/auth, and Qdrant decisions.
- **Acceptance criteria:** Unit/evaluation coverage for filters, citations, abstention, irrelevant/injection content, isolation attempts, and provider failures.
- **Status:** NOT STARTED.

### Backend Phase 4 — LangGraph workflow
- **Objective:** Add a small bounded workflow only if graph orchestration is justified.
- **Tasks:** Typed minimal state; validate/retrieve/assess/generate-or-abstain/return nodes; explicit bounded routes and fake-adapter tests.
- **Dependencies:** Phases 1–3; documented need for LangGraph over a simpler direct workflow.
- **Acceptance criteria:** Topology/state docs; node/route/failure/retry tests; no infinite loops or generation when evidence checks fail.
- **Status:** DEFERRED until a concrete orchestration requirement is confirmed.

### Backend Phase 5 — API streaming and client contract
- **Objective:** Define and implement a stable browser-facing API, optionally SSE if confirmed.
- **Tasks:** Version request/response/event schemas; errors, cancellation, disconnect, isolation, auth/rate limits; contract tests.
- **Dependencies:** Phases 1–3; confirmed tenant/auth and stream requirements.
- **Acceptance criteria:** Documented contract; successful/empty/error/disconnect/malformed/concurrent tests; end-to-end client contract test without browser secrets.
- **Status:** NOT STARTED; the existing widget expects SSE, but no compatible backend contract or stream implementation exists.

### Backend Phase 6 — Security, quality, and operations
- **Objective:** Apply controls for the actual deployment and document remaining risks.
- **Tasks:** Threat model; authorization/isolation; upload/limits; secret handling; redacted structured logs; dependency checks; CORS; retention; deployment/runbook as applicable.
- **Dependencies:** Deployment, auth, tenant, and data-retention decisions.
- **Acceptance criteria:** Evidence-backed applicable security checklist; critical tests/static checks pass; unresolved risks listed.
- **Status:** NOT STARTED.

### Backend Phase 7 — Evaluation and release readiness
- **Objective:** Establish measured RAG quality, runtime, cost, and failure baselines.
- **Tasks:** Versioned evaluation dataset; retrieval/grounding/citation/abstention/latency/provider-failure measures; realistic concurrency where required.
- **Dependencies:** Phases 2–6 and provider/product requirements.
- **Acceptance criteria:** Baselines and limitations documented; release claims match passing acceptance criteria.
- **Status:** NOT STARTED.

### UI Phase A — Audit and design direction
- **Objective:** Inventory the existing widget and propose a compact design system and state/component plan before broad restyling.
- **Tasks:** Preserve the Vue custom-element/Shadow DOM integration; document reusable components, Sass tokens, theme limitations, UX gaps, and the real API boundary.
- **Design direction:** Refined neutral surfaces with one restrained brand accent; semantic surface/text/border/status tokens; consistent type/spacing/radius/focus tokens; clear message hierarchy; responsive panel/composer; subtle motion respecting reduced-motion; use existing SVG/icon components, not emoji as core controls.
- **State/component inventory:** launcher; dialog/header/actions; empty state; conversation log/message; typing/streaming; complete; error/retry; unsupported/abstention; source citation (only with real metadata); composer/send/loading. Do not add conversation history, attachment, model-selection, or cancellation controls until backed by the product/API.
- **Dependencies:** Existing widget audit complete; agree a single API/SSE contract before wiring citations or unsupported-answer states.
- **Acceptance criteria:** Limitations and proposal recorded; no claim of visual validation without browser/screenshot checks.
- **Status:** Audit completed. The audit found fixed Sass colors despite runtime palette props, forced scroll-to-bottom on every update, plain-text response rendering, and generic canned suggestions that implied unverified workspace content.

### UI Phase B — Design system and core layout
- **Objective:** Apply reusable tokens and polish the widget layout while preserving framework and embedding behavior.
- **Tasks:** Make runtime palette behavior consistent; improve visual hierarchy, responsive panel/header/message/composer, focus and contrast.
- **Dependencies:** UI Phase A.
- **Acceptance criteria:** Verified at mobile/tablet/desktop widths; no host-page style leakage or broken widget behavior.
- **Status:** PARTIALLY COMPLETE. Runtime palette/surface tokens and core header/composer styling were updated and the SDK/client build passed; no visual checks across device sizes were performed.

### UI Phase C — Interaction states
- **Objective:** Improve real user-facing chat states without fake answers or decorative controls.
- **Tasks:** Correct follow-scroll behavior; readable long-form content; safe errors/retry; empty/loading/streaming/complete/offline/abstention states; real-source citations only; keyboard semantics.
- **Dependencies:** UI Phase A; API contract for backend-dependent states.
- **Acceptance criteria:** Keyboard, scrolling, copy/citation, error/retry, stream and empty states verified; no unsupported claims or fake source data.
- **Status:** PARTIALLY COMPLETE. Follow-scroll and safe HTTP error messaging were improved. Explicit retry, offline/abstention states, rich text/citations, and behavior verification remain outstanding.

### UI Phase D — Quality and regression
- **Objective:** Verify the supported widget experience and host integration.
- **Tasks:** Browser/layout checks, keyboard-only/focus/reduced-motion/contrast, long responses/code/tables/citations, stream failures and concurrent behavior; run existing build/tests.
- **Dependencies:** UI Phases B–C; restored frontend dependencies and available browser tooling.
- **Acceptance criteria:** Exact checks and outcomes recorded; no visual verification claim without visual evidence.
- **Status:** PARTIALLY COMPLETE for build validation only. The full build is blocked by the absent integration-portal workspace; browser, accessibility, contrast, and responsive checks are not run.

## 8. Security and Reliability Checklist

| Item | Status | Evidence / remaining work |
|---|---|---|
| Secret management | NOT ASSESSED | `.env.example` contains placeholders; actual `.env` contents were intentionally not inspected or recorded. Confirm tracked secret hygiene separately. |
| Authentication/authorization | NOT ASSESSED | No auth implementation found in inspected API entry point; define deployment model before protected data routes. |
| Tenant isolation | NOT ASSESSED | Current `company_id` check is a hard-coded stub; browser-supplied `app_id` cannot establish authorization. |
| Upload validation/path traversal | NOT STARTED | No upload endpoint implementation identified. |
| Prompt-injection defenses | NOT STARTED | No production retrieval/generation path identified. |
| Request/time/token limits and retries | NOT ASSESSED | No production provider calls to validate; define bounded limits during integration. |
| CORS | NOT ASSESSED | Origins listed in `.env.example` are not wired to the app; confirm actual deployment origins. |
| Logging/redaction | PARTIALLY VERIFIED | The working-tree app has no print-time logging; unexpected-error tests confirm internal details are not returned or logged by the handler. No production logging/retention policy exists. |
| Health/readiness information disclosure | PARTIALLY VERIFIED | `/health` and `/ready` return only fixed status values; docs state readiness checks only this API process because no external dependencies are wired. |
| Data retention/deletion | NOT STARTED | No production document/vector/conversation persistence identified. |
| Dependency vulnerability/lockfile hygiene | NEEDS WORK | The API foundation has a pinned lock; broader RAG requirements are lower-bounded. `npm ci` reported 13 dependency advisories (3 low, 4 moderate, 6 high); no `npm audit` investigation or Python vulnerability scan was run. |

## 9. Test and Validation Log

| Date | Exact command | Environment/context | Result | Notes |
|---|---|---|---|---|
| 2026-10-26 | `git status --short` | Repository root, audit start | PASS (exit 0) | Pre-existing changes: modified `narada-rag-backend/app/main.py`, untracked `tasks.md`; both were preserved and integrated. |
| 2026-10-26 | `npm run test:platform` | Repository root | PASS (exit 0; 0 tests) | Script invoked Node test runner for package paths; it reported 0 tests, so no behavior was verified. |
| 2026-10-26 | `npm run build` | Repository root before dependency restore | FAIL (exit 127) | SDK build initially stopped with `vite: not found`. |
| 2026-10-26 | `npm ci` | Repository root | PASS (exit 0) | Restored 451 workspace packages; npm reported 13 advisories (3 low, 4 moderate, 6 high). No audit fix was run. |
| 2026-10-26 | `npm run build` | Repository root, after `npm ci` | PARTIAL (exit 1) | SDK and four host-client builds completed; command then failed because there is no `narada-integration-portal` workspace. Sass emitted existing `@import` deprecation warnings. |
| 2026-10-26 | `npm run build:sdk && npm run build:clients` | Repository root, after final widget styling edits | PASS (exit 0) | SDK and all four host-client production builds completed; Sass still reports legacy `@import` deprecation warnings. |
| 2026-10-26 | `.venv/bin/python --version` | Repository root | PASS | Python 3.12.3. |
| 2026-10-26 | `.venv/bin/python -c "import importlib.util as u; names=('fastapi','pydantic','pydantic_settings','httpx','pytest','starlette'); print('\\n'.join(f'{name}: {bool(u.find_spec(name))}' for name in names))"` | Repository root, before install | PASS (probe ran) | All six imports were unavailable. |
| 2026-10-26 | `python -m pip --python .venv/bin/python install 'fastapi>=0.115' 'pydantic-settings>=2.5' 'httpx>=0.27'` | Repository root | PASS (exit 0) | Installed only the API foundation and ASGI test-client dependencies in the existing virtualenv, not the embedding/vector stack. |
| 2026-10-26 | `python -m pip --python .venv/bin/python install 'uvicorn>=0.30'` | Repository root | PASS (exit 0) | Installed the minimal server runtime for the startup check. |
| 2026-10-26 | `cd narada-rag-backend && ../.venv/bin/python -m unittest discover -s tests -v` | Python 3.12.3; no provider credentials | PASS (8 tests) | Covers settings validation, health/readiness/request IDs, validation bounds, HTTP errors, explicit 501 behavior, and generic error redaction. |
| 2026-10-26 | `cd narada-rag-backend && ../.venv/bin/python -m compileall -q app tests` | Python 3.12.3 | PASS (exit 0) | Backend and test modules compile. |
| 2026-10-26 | `python -m venv /tmp/narada-api-lock-check-20261026 && python -m pip --python /tmp/narada-api-lock-check-20261026/bin/python install -r narada-rag-backend/requirements-foundation.lock && cd narada-rag-backend && /tmp/narada-api-lock-check-20261026/bin/python -m unittest discover -s tests -v && /tmp/narada-api-lock-check-20261026/bin/python -m compileall -q app tests` | Clean Python 3.12 virtualenv | PASS (8 tests; compile pass) | Verified pinned foundation dependencies can be installed and test without relying on the existing project virtualenv. |
| 2026-10-26 | `cd narada-rag-backend && ../.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8093` | Local API; followed by `curl -i -sS http://127.0.0.1:8093/health` and `curl -i -sS http://127.0.0.1:8093/ready` | PASS | Server started; both endpoints returned 200 and JSON status, with `X-Request-ID`. Server stopped after verification. |
| 2026-10-26 | `git --no-pager diff --check` | Repository root | PASS (exit 0) | No whitespace errors. |

## 10. Decisions and Assumptions

### Confirmed by repository evidence
- The embeddable SDK is a Vue 2 custom element with Shadow DOM styles; host examples exist for HTML, React, Vue, and Angular.
- The widget currently posts `{app_id, query}` and requests `text/event-stream`; the client README describes the same expected shape.
- The backend currently does not implement that contract or a real RAG response.
- The working-tree API now exposes `/health`, `/ready`, and a validated `/api/chat` stub that returns 501 rather than fabricated output.

### Proposals, not decisions
- Keep the existing SDK and host examples; do not rebuild the UI in another framework.
- Build a small deterministic RAG workflow before adding agentic orchestration.
- Use FastAPI for the backend foundation because it is already in the repository.
- Prefer neutral premium surfaces, a single restrained accent, and reusable semantic tokens for the UI refresh.

### Unresolved
- **LLM provider:** Unconfirmed; explicitly decide whether xAI/Grok is required.
- **Qdrant:** Local vs hosted and lifecycle are unconfirmed.
- **Tenant model/auth:** Unconfirmed; never treat a browser-provided workspace ID as authorization.
- **Streaming:** Widget currently expects SSE, but event schema/version/error/cancellation semantics are unconfirmed.
- **Persistence:** Conversation/document storage and retention requirements are unconfirmed.
- **Supported document formats and deployment:** Unconfirmed.

## 11. Next 3 Actions

1. Complete the widget's high-priority UI acceptance checks with browser-based responsive, keyboard, contrast, and reduced-motion verification; add focused UI interaction tests.
2. Confirm provider, Qdrant, tenant/auth, and versioned SSE event-contract decisions before implementing ingestion, retrieval, generation, or citations.
3. Lock and validate the future RAG dependency set when its first ingestion/retrieval phase is selected; do not install or claim those packages prematurely.

## 12. Change Log

- 2026-10-26: Audited repository and corrected task statuses to match actual tracked/working-tree state; documented the Python API foundation, tests, setup guide, and API contract limitation.
- 2026-10-26: Added an exact-version API foundation lock and verified it in a clean virtual environment (8 tests pass).
- 2026-10-26: Improved widget theme switching, follow-scroll behavior, and HTTP error messaging; updated root and SDK documentation. SDK and host builds pass, while full workspace build remains blocked by the missing integration portal.
