<template>
  <div class="ui-field">
    <label v-if="label" class="ui-field__label" :for="inputId">
      {{ label }}<span v-if="required" class="ui-required" aria-hidden="true"> *</span>
    </label>
    <p v-if="description" class="ui-field__description" :id="`${inputId}-description`">{{ description }}</p>
    <div class="ui-select-wrap">
      <select
        :id="inputId"
        class="ui-select"
        :value="value"
        :disabled="disabled"
        :required="required"
        :aria-invalid="error ? 'true' : 'false'"
        :aria-describedby="error ? `${inputId}-error` : hint ? `${inputId}-hint` : null"
        @change="$emit('input', $event.target.value)"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option
          v-for="option in options"
          :key="option.value"
          :value="option.value"
          :disabled="option.disabled"
        >{{ option.label }}</option>
      </select>
      <span class="ui-select-chevron" aria-hidden="true">⌄</span>
    </div>
    <div class="ui-field__meta">
      <span v-if="error" class="ui-field__error" :id="`${inputId}-error`" role="alert">{{ error }}</span>
      <span v-else-if="hint" class="ui-field__hint" :id="`${inputId}-hint`">{{ hint }}</span>
    </div>
  </div>
</template>

<script>
let nextSelectId = 0;

export default {
  name: 'UiSelect',
  props: {
    id: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: '',
    },
    description: {
      type: String,
      default: '',
    },
    hint: {
      type: String,
      default: '',
    },
    error: {
      type: String,
      default: '',
    },
    value: {
      type: String,
      default: '',
    },
    options: {
      type: Array,
      default: () => [],
    },
    placeholder: {
      type: String,
      default: '',
    },
    required: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    nextSelectId += 1;
    return {
      generatedId: `narada-select-${nextSelectId}`,
    };
  },
  computed: {
    inputId() {
      return this.id || this.generatedId;
    },
  },
};
</script>
