import React from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';
import './style.css';

function App() {
  const [palette, setPalette] = useState('indigo-modern');
  const [theme, setTheme] = useState('light');

  return (
    <>
      <main className="page">
        <p className="eyebrow">React integration</p>
        <h1>One script.<br />Any frontend.</h1>
        <p className="intro">
          Narada runs as a native custom element, so your React app does not
          need to bundle or configure Vue 2.
        </p>
        <div className="code-card">
          <code>&lt;ai-chat-widget app-id="demo-workspace" /&gt;</code>
        </div>
        <div className="demo-controls" aria-label="Widget appearance controls">
          <label>
            Palette
            <select value={palette} onChange={(event) => setPalette(event.target.value)}>
              <option value="indigo-modern">Indigo Modern</option>
              <option value="ocean-blue">Ocean Blue</option>
              <option value="modern-sky-blue">Modern Sky Blue</option>
            </select>
          </label>
          <button
            type="button"
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
          >
            Switch to {theme === 'light' ? 'dark' : 'light'} theme
          </button>
        </div>
      </main>
      <ai-chat-widget
        app-id="demo-workspace"
        api-url="http://localhost:8000/api/chat"
        palette={palette}
        theme={theme}
      />
    </>
  );
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
