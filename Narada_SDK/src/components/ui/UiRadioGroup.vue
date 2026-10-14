<template>
  <fieldset
    class="ui-radio-group"
    role="radiogroup"
    :aria-invalid="error ? 'true' : 'false'"
    :aria-describedby="error ? `${groupId}-error` : description ? `${groupId}-description` : null"
  >
    <legend class="ui-field__label">{{ label }}<span v-if="required" class="ui-required" aria-hidden="true"> *</span></legend>
    <p v-if="description" class="ui-field__description" :id="`${groupId}-description`">{{ description }}</p>
    <div class="ui-radio-group__options">
      <label
        v-for="option in normalizedOptions"
        :key="option.value"
        class="ui-choice"
        :class="{ 'is-disabled': disabled || option.disabled }"
      >
        <input
          class="ui-choice__input"
          type="radio"
          :name="groupId"
          :value="option.value"
          :checked="value === option.value"
          :disabled="disabled || option.disabled"
          :aria-checked="String(value === option.value)"
          @change="$emit('input', option.value)"
        />
        <span class="ui-radio-mark" aria-hidden="true"></span>
        <span class="ui-choice__copy">
          <span class="ui-choice__label">{{ option.label }}</span>
          <span v-if="option.description" class="ui-choice__description">{{ option.description }}</span>
        </span>
      </label>
    </div>
    <span v-if="error" class="ui-field__error" :id="`${groupId}-error`" role="alert">{{ error }}</span>
  </fieldset>
</template>

<script>
let nextRadioGroupId = 0;

export default {
  name: 'UiRadioGroup',
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
    options: {
      type: Array,
      default: () => [],
    },
    value: {
      type: [String, Number],
      default: '',
    },
    error: {
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
    nextRadioGroupId += 1;
    return {
      generatedId: `narada-radio-group-${nextRadioGroupId}`,
    };
  },
  computed: {
    groupId() {
      return this.id || this.generatedId;
    },
    normalizedOptions() {
      return this.options.map((option) => {
        if (typeof option === 'string') {
          return { label: option, value: option, disabled: false };
        }

        return {
          label: option.label ?? String(option.value),
          value: option.value,
          disabled: Boolean(option.disabled),
          description: option.description || '',
        };
      });
    },
  },
};
</script>
