<template>
  <div class="widget-shell" :data-palette="palette" :data-theme="theme">
    <section
      v-if="isOpen"
      class="chat-panel"
      role="dialog"
      :aria-label="displayTitle"
    >
      <ChatHeader
        :title="displayTitle"
        :busy="isLoading"
        @close="isOpen = false"
        @reset="resetConversation"
      />
      <MessageList
        :messages="messages"
        :is-loading="isLoading"
        :welcome-message="welcomeMessage"
        :assistant-name="displayTitle"
        @suggestion="sendMessage"
        @rate="rateMessage"
      />
      <ChatInput :disabled="isLoading" @send="sendMessage" />
    </section>
    <button
      type="button"
      class="launcher"
      :class="{ 'launcher--open': isOpen }"
      :aria-label="isOpen ? 'Close chat' : 'Open AI chat'"
      :aria-expanded="isOpen ? 'true' : 'false'"
      @click="isOpen = !isOpen"
    >
      <span v-if="!isOpen" class="launcher__label">Chat with {{ displayTitle }}</span>
      <span class="launcher__icon" aria-hidden="true">
        <svg v-if="!isOpen" viewBox="0 0 24 24" fill="none">
          <path d="M5 18.5 3.5 21l4.2-1.2a9 9 0 1 0-2.7-1.3Z" />
          <path d="M8 10h8M8 14h5" />
        </svg>
        <span v-else>×</span>
      </span>
    </button>
  </div>
</template>

<script>
import ChatHeader from './ChatHeader.vue';
import ChatInput from './ChatInput.vue';
import MessageList from './MessageList.vue';

const MAX_ERROR_LENGTH = 400;

export default {
  name: 'ChatContainer',
  components: {
    ChatHeader,
    ChatInput,
    MessageList,
  },
  props: {
    appId: {
      type: String,
      default: '',
    },
    apiUrl: {
      type: String,
      default: '/api/chat',
    },
    title: {
      type: String,
      default: 'AI Assistant',
    },
    welcomeMessage: {
      type: String,
      default: 'Ask a question to get started.',
    },
    palette: {
      type: String,
      default: 'indigo-modern',
    },
    theme: {
      type: String,
      default: 'light',
    },
  },
  data() {
    return {
      isOpen: false,
      isLoading: false,
      messages: [],
      activeController: null,
      nextMessageId: 0,
    };
  },
  beforeDestroy() {
    if (this.activeController) {
      this.activeController.abort();
    }
  },
  computed: {
    displayTitle() {
      return this.title.trim() || 'AI Assistant';
    },
  },
  methods: {
    rateMessage({ id, value }) {
      const message = this.messages.find((item) => item.id === id);
      if (message) {
        message.rating = value;
      }
    },
    resetConversation() {
      if (this.isLoading) {
        return;
      }
      this.messages.splice(0, this.messages.length);
    },
    async sendMessage(query) {
      if (this.isLoading) {
        return;
      }

      const messageId = ++this.nextMessageId;
      const userMessage = {
        id: `${messageId}-user`,
        role: 'user',
        content: query,
        createdAt: new Date().toISOString(),
      };
      const assistantMessage = {
        id: `${messageId}-assistant`,
        role: 'assistant',
        content: '',
        rating: 0,
        createdAt: new Date().toISOString(),
      };
      this.messages.push(userMessage, assistantMessage);
      const assistantIndex = this.messages.length - 1;
      this.isLoading = true;

      try {
        if (!this.appId.trim()) {
          throw new Error('Chat is not configured: set the app-id attribute.');
        }
        if (!this.apiUrl.trim()) {
          throw new Error('Chat is not configured: set a valid api-url.');
        }

        this.activeController = new AbortController();
        const response = await fetch(this.apiUrl, {
          method: 'POST',
          headers: {
            Accept: 'text/event-stream',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            app_id: this.appId,
            query,
          }),
          signal: this.activeController.signal,
        });

        if (!response.ok) {
          const responseBody = await response.text();
          const detail = responseBody.trim().slice(0, MAX_ERROR_LENGTH);
          throw new Error(
            `Chat request failed (${response.status})${detail ? `: ${detail}` : ''}`,
          );
        }
        if (!response.body || typeof response.body.getReader !== 'function') {
          throw new Error('Chat response does not support streaming.');
        }

        await this.readEventStream(response.body.getReader(), assistantIndex);
        if (!this.messages[assistantIndex].content) {
          this.messages[assistantIndex].content = 'The assistant returned an empty response.';
        }
      } catch (error) {
        if (!error || error.name !== 'AbortError') {
          if (this.activeController) {
            this.activeController.abort();
          }
          const message = error && error.message
            ? error.message
            : 'An unexpected error occurred while contacting the assistant.';
          this.messages[assistantIndex].content = `Sorry, ${message}`;
        }
      } finally {
        this.activeController = null;
        this.isLoading = false;
      }
    },
    async readEventStream(reader, assistantIndex) {
      const decoder = new TextDecoder();
      let lineBuffer = '';
      let dataLines = [];

      const dispatchEvent = () => {
        if (dataLines.length === 0) {
          return;
        }

        const eventData = dataLines.join('\n');
        dataLines = [];
        this.appendEventData(eventData, assistantIndex);
      };

      const processLine = (line) => {
        if (line === '') {
          dispatchEvent();
          return;
        }
        if (line.startsWith(':')) {
          return;
        }
        if (line.startsWith('data:')) {
          dataLines.push(line.slice(5).replace(/^ /, ''));
        }
      };

      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          break;
        }

        lineBuffer += decoder.decode(value, { stream: true });
        let newlineIndex = lineBuffer.indexOf('\n');
        while (newlineIndex !== -1) {
          let line = lineBuffer.slice(0, newlineIndex);
          if (line.endsWith('\r')) {
            line = line.slice(0, -1);
          }
          processLine(line);
          lineBuffer = lineBuffer.slice(newlineIndex + 1);
          newlineIndex = lineBuffer.indexOf('\n');
        }
      }

      lineBuffer += decoder.decode();
      if (lineBuffer) {
        processLine(lineBuffer.endsWith('\r') ? lineBuffer.slice(0, -1) : lineBuffer);
      }
      dispatchEvent();
    },
    appendEventData(eventData, assistantIndex) {
      if (eventData === '[DONE]') {
        return;
      }

      let payload;
      try {
        payload = JSON.parse(eventData);
      } catch (error) {
        throw new Error('The chat service sent an invalid streaming event.');
      }

      const choice = payload && payload.choices && payload.choices[0];
      const token = payload && (
        payload.token
        || payload.delta
        || payload.content
        || payload.answer
        || (choice && choice.delta && choice.delta.content)
        || (choice && choice.text)
      );

      if (typeof token === 'string' && token) {
        this.messages[assistantIndex].content += token;
      }
    },
  },
};
</script>
