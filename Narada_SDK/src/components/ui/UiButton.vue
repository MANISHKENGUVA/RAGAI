<template>
  <button
    class="ui-button"
    :class="[`ui-button--${variant}`, `ui-button--${size}`, { 'is-loading': loading }]"
    :type="type"
    :disabled="disabled || loading"
    :aria-busy="loading ? 'true' : null"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="ui-spinner" aria-hidden="true"></span>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'UiButton',
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'outlined', 'ghost', 'destructive', 'link'].includes(value),
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value),
    },
    type: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
