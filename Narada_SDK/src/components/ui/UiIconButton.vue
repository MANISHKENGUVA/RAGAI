<template>
  <button
    class="ui-icon-button"
    :class="`ui-icon-button--${size}`"
    type="button"
    :aria-label="label"
    :title="tooltip || label"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'UiIconButton',
  props: {
    label: {
      type: String,
      required: true,
    },
    tooltip: {
      type: String,
      default: '',
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
