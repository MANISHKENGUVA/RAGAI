<template>
  <div class="ui-field">
    <label v-if="label" class="ui-field__label" :for="inputId">
      {{ label }}<span v-if="required" class="ui-required" aria-hidden="true"> *</span>
    </label>
    <p v-if="description" class="ui-field__description" :id="`${inputId}-description`">
      {{ description }}
    </p>
    <div class="ui-field__control" :class="{ 'has-error': Boolean(error) }">
      <span v-if="$slots.leading" class="ui-field__leading" aria-hidden="true"><slot name="leading"></slot></span>
      <input
        :id="inputId"
        class="ui-text-field"
        :type="type"
        :value="value"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :readonly="readonly"
        :maxlength="maxlength || null"
        :aria-invalid="error ? 'true' : 'false'"
        :aria-describedby="describedBy"
        @input="$emit('input', $event.target.value)"
      />
      <button
        v-if="clearable && value && !disabled && !readonly"
        class="ui-field__clear"
        type="button"
        :aria-label="`Clear ${label || 'input'}`"
        @click="$emit('input', '')"
      >×</button>
      <span v-if="$slots.trailing" class="ui-field__trailing" aria-hidden="true"><slot name="trailing"></slot></span>
    </div>
    <div class="ui-field__meta">
      <span v-if="error" class="ui-field__error" :id="`${inputId}-error`" role="alert">{{ error }}</span>
      <span v-else-if="hint" class="ui-field__hint" :id="`${inputId}-hint`">{{ hint }}</span>
      <span v-if="maxlength" class="ui-field__counter" :class="{ 'is-limit': value.length >= maxlength }">
        {{ value.length }} / {{ maxlength }}
      </span>
    </div>
  </div>
</template>

<script>
let nextFieldId = 0;

export default {
  name: 'UiTextField',
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
    type: {
      type: String,
      default: 'text',
      validator: (value) => ['text', 'email', 'password', 'number', 'search', 'url', 'tel'].includes(value),
    },
    placeholder: {
      type: String,
      default: '',
    },
    maxlength: {
      type: Number,
      default: 0,
    },
    required: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    nextFieldId += 1;
    return {
      generatedId: `narada-field-${nextFieldId}`,
    };
  },
  computed: {
    inputId() {
      return this.id || this.generatedId;
    },
    describedBy() {
      if (this.error) {
        return `${this.inputId}-error`;
      }
      return this.description
        ? `${this.inputId}-description`
        : this.hint
          ? `${this.inputId}-hint`
          : null;
    },
  },
};
</script>
