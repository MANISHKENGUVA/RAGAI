<template>
  <div class="chat-composer">
    <form class="chat-input" aria-label="Send a message" @submit.prevent="submit">
      <UiTextarea
        id="chat-query"
        label="Your message"
        v-model="query"
        class="chat-input__field"
        :disabled="disabled"
        rows="1"
        maxlength="4000"
        placeholder="Message Narada..."
        @keydown.enter.exact.prevent="submit"
      />
      <UiButton
        type="submit"
        size="lg"
        :disabled="disabled || !query.trim()"
        :loading="disabled"
        aria-label="Send message"
      >
        <span class="chat-input__send-icon" aria-hidden="true">↑</span>
      </UiButton>
    </form>
    <div class="chat-composer__footer">
      <span>Enter to send <span aria-hidden="true">·</span> Shift + Enter for a new line</span>
      <span class="chat-composer__powered">Powered by <strong>Narada</strong></span>
    </div>
  </div>
</template>

<script>
import UiButton from './ui/UiButton.vue';
import UiTextarea from './ui/UiTextarea.vue';

export default {
  name: 'ChatInput',
  components: {
    UiButton,
    UiTextarea,
  },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      query: '',
    };
  },
  methods: {
    submit() {
      const query = this.query.trim();
      if (!query || this.disabled) {
        return;
      }

      this.$emit('send', query);
      this.query = '';
    },
  },
};
</script>
