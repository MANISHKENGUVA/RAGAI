<template>
  <label class="ui-choice" :class="{ 'is-disabled': disabled, 'has-error': Boolean(error) }">
    <input
      ref="checkbox"
      class="ui-choice__input"
      type="checkbox"
      :checked="checked"
      :disabled="disabled"
      :aria-invalid="error ? 'true' : 'false'"
      :aria-describedby="error ? `${inputId}-error` : null"
      @change="$emit('input', $event.target.checked)"
    />
    <span class="ui-checkbox-mark" aria-hidden="true"><span>✓</span></span>
    <span class="ui-choice__copy">
      <span class="ui-choice__label">{{ label }}</span>
      <span v-if="description" class="ui-choice__description">{{ description }}</span>
      <span v-if="error" class="ui-field__error" :id="`${inputId}-error`" role="alert">{{ error }}</span>
    </span>
  </label>
</template>

<script>
let nextCheckboxId = 0;

export default {
  name: 'UiCheckbox',
  props: {
    id: {
      type: String,
      default: '',
    },
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
    indeterminate: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: '',
    },
  },
  data() {
    nextCheckboxId += 1;
    return {
      generatedId: `narada-checkbox-${nextCheckboxId}`,
    };
  },
  computed: {
    inputId() {
      return this.id || this.generatedId;
    },
  },
  mounted() {
    this.syncIndeterminate();
  },
  updated() {
    this.syncIndeterminate();
  },
  methods: {
    syncIndeterminate() {
      if (this.$refs.checkbox) {
        this.$refs.checkbox.indeterminate = this.indeterminate;
      }
    },
  },
};
</script>
