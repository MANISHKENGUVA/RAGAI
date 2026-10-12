<template>
  <fieldset class="ui-rating" :disabled="disabled">
    <legend class="ui-field__label">{{ label }}</legend>
    <div class="ui-rating__stars" role="radiogroup" :aria-label="label">
      <button
        v-for="star in max"
        :key="star"
        class="ui-rating__star"
        :class="{ 'is-selected': star <= value }"
        type="button"
        role="radio"
        :aria-checked="value === star ? 'true' : 'false'"
        :aria-label="`Rate ${star} of ${max} stars`"
        :disabled="disabled"
        @click="$emit('input', star)"
      >★</button>
    </div>
    <span v-if="value" class="ui-rating__value">{{ value }} / {{ max }}</span>
  </fieldset>
</template>

<script>
export default {
  name: 'UiRating',
  props: {
    label: {
      type: String,
      default: 'Rating',
    },
    value: {
      type: Number,
      default: 0,
      validator: (value) => Number.isInteger(value) && value >= 0,
    },
    max: {
      type: Number,
      default: 5,
      validator: (value) => Number.isInteger(value) && value > 0,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
