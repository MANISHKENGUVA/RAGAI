# Narada SDK client examples

This folder contains runnable examples that all use the single Vite-built SDK in `../Narada_SDK`:

- `NORMALHTMLCLIENT` - plain HTML served by Vite
- `REACTCLIENT` - React + Vite
- `VUECLIENT` - Vue 3 + Vite
- `ANGULARCLIENT` - Angular standalone application

## Install and build

From the repository root, install the complete workspace once:

```sh
npm install
```

Build the SDK and all four client apps:

```sh
npm run build:sdk
npm run build:clients
```

The aggregate `npm run build` also invokes an integration-portal workspace
that is not present in this checkout and therefore does not complete.

Each client has `predev` and `prebuild` steps that rebuild the SDK and copy
only the bundle it loads, `Narada_SDK/dist/ai-chat-widget.iife.js`, and its
source map into that client’s ignored `public/` folder. The client page loads
the custom element as a regular script; the client framework does not need to
depend on Vue 2 or load the UMD/minified variants.

## Run a client

Run any one client or the integration portal from the repository root:

```sh
npm run dev:html
npm run dev:react
npm run dev:vue
npm run dev:angular
npm run dev:portal
```

Vite and Angular print the local URL when the dev server starts.

## Configure the RAG backend

The examples use `app-id="demo-workspace"` and `api-url="http://localhost:8000/api/chat"`. Update those values in the relevant app's `index.html` if your workspace ID or backend URL differs. The backend must accept a JSON `POST` body shaped like `{"app_id":"demo-workspace","query":"..."}`, allow the client origin through CORS, and stream SSE events. See [the SDK guide](../Narada_SDK/README.md) for the supported response payloads.

## Integration portal

`stitch_narada_chat_widget_sdk` contains the runnable Narada Widget Studio.
Its customizer applies the Indigo Modern, Ocean Blue, and Modern Sky Blue
palettes independently from the light/dark surface theme, and its integration
view generates plain HTML, React, Vue 3, and Angular snippets with each
framework's native attribute binding style.
