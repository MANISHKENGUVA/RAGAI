<template>
  <label class="ui-switch-row" :class="{ 'is-disabled': disabled }">
    <span class="ui-choice__copy">
      <span class="ui-choice__label">{{ label }}</span>
      <span v-if="description" class="ui-choice__description">{{ description }}</span>
    </span>
    <input
      class="ui-switch-input"
      type="checkbox"
      role="switch"
      :checked="checked"
      :disabled="disabled"
      :aria-label="label"
      @change="$emit('input', $event.target.checked)"
    />
    <span class="ui-switch-track" aria-hidden="true"><span class="ui-switch-thumb"></span></span>
  </label>
</template>

<script>
export default {
  name: 'UiSwitch',
  props: {
    label: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      default: '',
    },
    checked: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
