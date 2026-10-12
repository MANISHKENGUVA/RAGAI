<template>
  <main class="page">
    <p class="eyebrow">Vue integration</p>
    <h1>Bring AI into your Vue app.</h1>
    <p class="intro">
      The chat widget is a native custom element. This Vue 3 app uses the
      prebuilt Vue 2 SDK without coupling the two Vue runtimes.
    </p>
    <div class="code-card">
      <code>&lt;ai-chat-widget app-id="demo-workspace"&gt;&lt;/ai-chat-widget&gt;</code>
    </div>
    <div class="demo-controls" aria-label="Widget appearance controls">
      <label>
        Palette
        <select v-model="palette">
          <option value="indigo-modern">Indigo Modern</option>
          <option value="ocean-blue">Ocean Blue</option>
          <option value="modern-sky-blue">Modern Sky Blue</option>
        </select>
      </label>
      <button type="button" @click="toggleTheme">
        Switch to {{ theme === 'light' ? 'dark' : 'light' }} theme
      </button>
    </div>
    <ai-chat-widget
      app-id="demo-workspace"
      api-url="http://localhost:8000/api/chat"
      :palette="palette"
      :theme="theme"
    ></ai-chat-widget>
  </main>
</template>

<script setup>
import { ref } from 'vue';

const palette = ref('indigo-modern');
const theme = ref('light');

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
}
</script>
