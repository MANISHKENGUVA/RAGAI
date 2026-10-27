<template>
  <header class="chat-header">
    <div class="chat-brand">
      <span class="chat-brand__mark" aria-hidden="true">✦</span>
      <div class="chat-brand__copy">
        <h2 class="chat-title">{{ resolvedTitle }}</h2>
        <p class="chat-subtitle">Ask a question to get started</p>
      </div>
    </div>
    <div class="chat-header__actions">
      <UiIconButton
        label="Start a new conversation"
        tooltip="New conversation"
        size="sm"
        :disabled="busy"
        @click="$emit('reset')"
      ><span aria-hidden="true">↻</span></UiIconButton>
      <UiIconButton
        label="Close chat"
        tooltip="Close chat"
        size="sm"
        @click="$emit('close')"
      ><span aria-hidden="true">×</span></UiIconButton>
    </div>
  </header>
</template>

<script>
import UiIconButton from './ui/UiIconButton.vue';

export default {
  name: 'ChatHeader',
  components: {
    UiIconButton,
  },
  props: {
    title: {
      type: String,
      default: '🤖 AI Assistant',
    },
    busy: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    resolvedTitle() {
      return typeof this.title === 'string' && this.title.trim()
        ? this.title.trim()
        : 'AI Assistant';
    },
  },
};
</script>
