# Narada AI Chat Widget SDK

Vue 2 embeddable chat widget registered as the `<ai-chat-widget>` custom element. Its UI and bundled styles are mounted in a Shadow DOM so host-page CSS does not style the widget and widget styles do not leak into the host page.

## Build

Requires Node.js 20.19 or newer (or 22.12 or newer) and npm.

```sh
npm install
npm run build
```

The Vite library build emits unminified and minified IIFE and UMD scripts:
`dist/ai-chat-widget.iife.js`, `dist/ai-chat-widget.iife.min.js`,
`dist/ai-chat-widget.umd.js`, and `dist/ai-chat-widget.umd.min.js`. Each script
has a corresponding source map. Vue and `vue-custom-element` are bundled, so
host pages do not need to load Vue separately. The build replaces Vue's
`process.env.NODE_ENV` checks, so the browser bundle does not require a
`process` polyfill. Widget and UI component Sass is imported as inline text and
added to each custom element's Shadow DOM when its Vue instance is created. The
build does not emit a separate CSS file.

## Embed in a host page

Publish or host `dist/ai-chat-widget.iife.js` on a URL accessible to the host website. The browser must support Custom Elements, Shadow DOM, `fetch`, `ReadableStream`, `TextDecoder`, and `AbortController`.

```html
<script
  defer
  src="https://cdn.example.com/ai-chat-widget.iife.js"
></script>

<ai-chat-widget
  app-id="your_workspace_id"
  api-url="https://api.example.com/chat"
  title="Narada Assistant"
  welcome-message="Hi! What can I help you with?"
  palette="indigo-modern"
  theme="light"
></ai-chat-widget>
```

`api-url` is optional and defaults to `/api/chat` relative to the host page. The endpoint must accept a cross-origin JSON `POST` where applicable and return a streamed response in Server-Sent Events format. Each event should use a JSON `data:` payload separated from the next event by a blank line. Supported token properties are `token`, `delta`, `content`, `answer`, `choices[0].delta.content`, and `choices[0].text`. A terminal `data: [DONE]` event is optional.

Example event stream:

```text
data: {"token":"Hello"}

data: {"token":" there!"}

data: [DONE]

```

The widget sends `{"app_id":"your_workspace_id","query":"..."}` with `Accept: text/event-stream` and `Content-Type: application/json`. Configure the backend's CORS policy to allow the embedding website's origin.

### Widget attributes

| Attribute | Default | Description |
| --- | --- | --- |
| `app-id` | empty | Workspace ID sent to the chat endpoint. Required to send messages. |
| `api-url` | `/api/chat` | Endpoint that accepts the streamed chat request. |
| `title` | `AI Assistant` | Chat panel heading. |
| `welcome-message` | `Ask a question to get started.` | Empty-conversation prompt. |
| `palette` | `indigo-modern` | Primary palette: `indigo-modern`, `ocean-blue`, or `modern-sky-blue`. |
| `theme` | `light` | Surface theme: `light` or `dark`, independent of the primary palette. |

Update `palette` and `theme` attributes at runtime to change the widget without
rebuilding it:

```js
const widget = document.querySelector('ai-chat-widget');
widget.setAttribute('palette', 'ocean-blue');
widget.setAttribute('theme', 'dark');
```

## Reusable UI components

The SDK entry exposes the ten Vue 2 components from `src/components/ui/` under
`NaradaAIChatWidget.uiComponents`:

| Component | Main use |
| --- | --- |
| `UiButton` | Primary, secondary, outlined, ghost, destructive, link, loading, and disabled actions. |
| `UiIconButton` | Tooltip-enabled icon-only actions with required accessible labels. |
| `UiTextField` | Labeled text, email, password, number, search, URL, and telephone fields. |
| `UiTextarea` | Labeled multiline input with descriptions and optional character limits. |
| `UiSelect` | Labeled native select with placeholder, disabled options, and validation. |
| `UiCheckbox` | Checked, unchecked, indeterminate, disabled, and error states. |
| `UiRadioGroup` | Labeled single-choice groups. |
| `UiSwitch` | Labeled preference toggles. |
| `UiDatePicker` | Calendar picker with bounds, clear/today/apply actions, and arrow-key day navigation. |
| `UiRating` | Labeled star rating control. |

The SDK also registers `<narada-ui-gallery>`, an interactive Shadow-DOM
showcase of all ten components. Its palette and theme attributes use the same
semantic colors as `<ai-chat-widget>`.

## SPA usage

Add the script once to the application's HTML shell. Render the custom element
in your SPA using that framework's custom-element support. React can bind
`palette` and `theme` props, Vue can bind `:palette` and `:theme`, and Angular
can bind `[attr.palette]` and `[attr.theme]`. Angular components must allow the
tag with `CUSTOM_ELEMENTS_SCHEMA`; Vue 3 projects should configure Vite's
`isCustomElement` compiler option. The SDK is framework-agnostic at runtime;
host applications do not need to install Vue 2.
