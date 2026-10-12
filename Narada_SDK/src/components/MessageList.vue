<template>
  <div ref="messageList" class="message-list" role="log" aria-live="polite" aria-relevant="additions text">
    <section v-if="messages.length === 0" class="welcome-card" aria-labelledby="welcome-title">
      <div class="welcome-card__intro">
        <span class="welcome-card__sparkle" aria-hidden="true">✦</span>
        <div>
          <p class="welcome-card__eyebrow">HELLO THERE</p>
          <h3 id="welcome-title" class="welcome-card__title">How can I help you today?</h3>
          <p class="welcome-card__copy">{{ welcomeMessage }}</p>
        </div>
      </div>
      <div class="welcome-card__suggestion-heading">
        <span>Try asking</span>
        <span class="welcome-card__suggestion-count">3 suggestions</span>
      </div>
      <div class="welcome-card__suggestions" aria-label="Suggested questions">
        <UiButton
          v-for="prompt in suggestedPrompts"
          :key="prompt.query"
          variant="ghost"
          class="suggestion-card"
          @click="$emit('suggestion', prompt.query)"
        >
          <span class="suggestion-card__icon" aria-hidden="true">{{ prompt.icon }}</span>
          <span class="suggestion-card__copy">
            <span class="suggestion-card__title">{{ prompt.title }}</span>
            <span class="suggestion-card__description">{{ prompt.description }}</span>
          </span>
          <span class="suggestion-card__arrow" aria-hidden="true">→</span>
        </UiButton>
      </div>
    </section>
    <div v-if="messages.length" class="conversation-date"><span>Today</span></div>
    <div
      v-for="(message, index) in messages"
      :key="message.id || index"
      class="message-row"
      :class="`message-row--${message.role}`"
    >
      <span v-if="message.role === 'assistant'" class="message-avatar" aria-hidden="true">✦</span>
      <div class="message-content">
        <p class="message-author">{{ message.role === 'assistant' ? assistantName : 'You' }}</p>
        <p class="message-bubble" :class="`message-bubble--${message.role}`">
          {{ message.content }}
        </p>
        <time v-if="message.createdAt" class="message-time" :datetime="message.createdAt">
          {{ formatTimestamp(message.createdAt) }}
        </time>
        <UiRating
          v-if="message.role === 'assistant' && message.content && (!isLoading || index < messages.length - 1)"
          class="message-rating"
          label="Was this answer helpful?"
          :value="message.rating"
          @input="$emit('rate', { id: message.id, value: $event })"
        />
      </div>
    </div>
    <div v-if="isLoading" class="message-row message-row--assistant">
      <span class="message-avatar" aria-hidden="true">✦</span>
      <div class="message-content">
        <p class="message-author">{{ assistantName }}</p>
        <p class="typing-indicator" aria-label="Assistant is responding">
          <span></span><span></span><span></span>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import UiButton from './ui/UiButton.vue';
import UiRating from './ui/UiRating.vue';

export default {
  name: 'MessageList',
  components: {
    UiButton,
    UiRating,
  },
  props: {
    messages: {
      type: Array,
      required: true,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    welcomeMessage: {
      type: String,
      default: 'Ask a question to get started.',
    },
    assistantName: {
      type: String,
      default: 'AI Assistant',
    },
  },
  data() {
    return {
      suggestedPrompts: [
        {
          title: 'Answer a question',
          description: 'Get a clear answer to something you are curious about.',
          query: 'What can you help me with?',
          icon: '?',
        },
        {
          title: 'Explain something',
          description: 'Break down a complex topic into simple steps.',
          query: 'Explain something to me',
          icon: '✦',
        },
        {
          title: 'Help me get started',
          description: 'Find the information you need in your workspace.',
          query: 'Help me get started',
          icon: '↗',
        },
      ],
    };
  },
  watch: {
    messages: {
      deep: true,
      handler() {
        this.scrollToBottom();
      },
    },
    isLoading() {
      this.scrollToBottom();
    },
  },
  updated() {
    this.scrollToBottom();
  },
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      if (Number.isNaN(date.getTime())) {
        return '';
      }
      return new Intl.DateTimeFormat(undefined, {
        hour: 'numeric',
        minute: '2-digit',
      }).format(date);
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const list = this.$refs.messageList;
        if (list) {
          list.scrollTop = list.scrollHeight;
        }
      });
    },
  },
};
</script>
