<template>
  <div class="ui-field">
    <label v-if="label" class="ui-field__label" :for="inputId">
      {{ label }}<span v-if="required" class="ui-required" aria-hidden="true"> *</span>
    </label>
    <p v-if="description" class="ui-field__description" :id="`${inputId}-description`">{{ description }}</p>
    <textarea
      :id="inputId"
      class="ui-textarea"
      :value="value"
      :placeholder="placeholder"
      :rows="rows"
      :maxlength="maxlength || null"
      :disabled="disabled"
      :readonly="readonly"
      :aria-invalid="error ? 'true' : 'false'"
      :aria-describedby="error ? `${inputId}-error` : description ? `${inputId}-description` : null"
      @input="$emit('input', $event.target.value)"
      @keydown="$emit('keydown', $event)"
    ></textarea>
    <div class="ui-field__meta">
      <span v-if="error" class="ui-field__error" :id="`${inputId}-error`" role="alert">{{ error }}</span>
      <span v-else-if="hint" class="ui-field__hint">{{ hint }}</span>
      <span v-if="maxlength" class="ui-field__counter" :class="{ 'is-limit': value.length >= maxlength }">
        {{ value.length }} / {{ maxlength }}
      </span>
    </div>
  </div>
</template>

<script>
let nextTextareaId = 0;

export default {
  name: 'UiTextarea',
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
    placeholder: {
      type: String,
      default: '',
    },
    rows: {
      type: Number,
      default: 3,
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
  },
  data() {
    nextTextareaId += 1;
    return {
      generatedId: `narada-textarea-${nextTextareaId}`,
    };
  },
  computed: {
    inputId() {
      return this.id || this.generatedId;
    },
  },
};
</script>
