<template>
  <main class="widget-shell ui-gallery" :data-palette="palette" :data-theme="activeTheme">
    <header class="ui-gallery__heading">
      <div>
        <p class="ui-gallery__eyebrow">NARADA CHAT · COMPONENT LIBRARY</p>
        <h1>Reusable chat components</h1>
        <p class="ui-gallery__intro">
          Ten accessible building blocks. Change the palette and surface theme independently.
        </p>
      </div>
      <div class="ui-gallery__theme-label">
        <span class="ui-gallery__palette-dot"></span>
        {{ paletteLabel }} <span aria-hidden="true">·</span> {{ themeLabel }}
      </div>
    </header>

    <section class="ui-gallery__grid" aria-label="Narada UI component examples">
      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>01</span><div><h2>Button</h2><p>Variants, sizes, and feedback states</p></div></div>
        <div class="ui-gallery__examples ui-gallery__button-row">
          <UiButton>Primary</UiButton>
          <UiButton variant="secondary">Secondary</UiButton>
          <UiButton variant="outlined">Outlined</UiButton>
          <UiButton variant="ghost">Ghost</UiButton>
          <UiButton variant="destructive">Delete</UiButton>
          <UiButton variant="link">Learn more</UiButton>
        </div>
        <div class="ui-gallery__examples ui-gallery__button-row">
          <UiButton size="xs">Extra small</UiButton>
          <UiButton size="sm" variant="secondary">Small</UiButton>
          <UiButton size="lg">Large</UiButton>
          <UiButton size="xl" variant="outlined">Extra large</UiButton>
          <UiButton loading>Submitting</UiButton>
          <UiButton disabled>Disabled</UiButton>
        </div>
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>02</span><div><h2>Icon button</h2><p>Named controls with hover tooltips</p></div></div>
        <div class="ui-gallery__examples ui-gallery__icon-row">
          <UiIconButton label="Start a new conversation" tooltip="New conversation"><span aria-hidden="true">＋</span></UiIconButton>
          <UiIconButton label="Open chat settings" tooltip="Settings"><span aria-hidden="true">⚙</span></UiIconButton>
          <UiIconButton label="Copy response" tooltip="Copy response" size="sm"><span aria-hidden="true">▣</span></UiIconButton>
          <UiIconButton label="Close" tooltip="Close" size="lg"><span aria-hidden="true">×</span></UiIconButton>
          <UiIconButton label="Unavailable action" disabled><span aria-hidden="true">↗</span></UiIconButton>
        </div>
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>03</span><div><h2>Text field</h2><p>Input types, help, validation, and states</p></div></div>
        <div class="ui-gallery__form-grid">
          <UiTextField label="Full name" placeholder="Enter your full name" description="Enter your name as you would like it displayed." required v-model="fullName" />
          <UiTextField label="Email address" type="email" value="not-an-email" error="Enter a valid email address." />
          <UiTextField label="Password" type="password" placeholder="Enter your password" hint="Use at least 8 characters." />
          <UiTextField label="Search" type="search" placeholder="Search..." clearable v-model="search" />
          <UiTextField label="Disabled" value="Unavailable" disabled />
          <UiTextField label="Read only" value="Support workspace" readonly />
        </div>
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>04</span><div><h2>Textarea</h2><p>Multiline text with a live character count</p></div></div>
        <UiTextarea
          label="Additional details"
          description="Tell the assistant anything else that might help."
          placeholder="Tell us more..."
          :maxlength="300"
          v-model="details"
        />
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>05</span><div><h2>Select</h2><p>Accessible native select with validation</p></div></div>
        <div class="ui-gallery__form-grid">
          <UiSelect label="Choose a topic" placeholder="Select an option" :options="topics" v-model="topic" />
          <UiSelect label="Language" value="en" :options="languages" />
          <UiSelect label="Required selection" placeholder="Select an option" :options="topics" error="Please choose a topic." required />
        </div>
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>06</span><div><h2>Checkbox</h2><p>Selection, indeterminate, and validation states</p></div></div>
        <div class="ui-gallery__choice-stack">
          <UiCheckbox label="Remember my preference" v-model="remember" />
          <UiCheckbox label="I agree to the terms and conditions" checked />
          <UiCheckbox label="Select all topics" indeterminate />
          <UiCheckbox label="Unavailable preference" disabled />
          <UiCheckbox label="Consent required" error="Please provide consent to continue." />
        </div>
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>07</span><div><h2>Radio group</h2><p>One selection from a related set of choices</p></div></div>
        <UiRadioGroup
          label="How would you like to continue?"
          :options="contactOptions"
          v-model="contactMethod"
        />
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>08</span><div><h2>Switch</h2><p>Toggle a preference on or off</p></div></div>
        <div class="ui-gallery__switch-stack">
          <UiSwitch label="Dark mode" description="Preview the widget's dark surface." :checked="activeTheme === 'dark'" @input="changeTheme" />
          <UiSwitch label="Show timestamps" checked />
          <UiSwitch label="Unavailable setting" disabled />
        </div>
      </article>

      <article class="ui-gallery__card ui-gallery__card--calendar">
        <div class="ui-gallery__card-heading"><span>09</span><div><h2>Date picker</h2><p>Keyboard-friendly calendar with min/max date support</p></div></div>
        <UiDatePicker label="Preferred date" hint="Choose a date that works for you." v-model="preferredDate" />
        <p class="ui-gallery__date-note">The date picker opens a calendar. Use arrow keys to move by day or week.</p>
      </article>

      <article class="ui-gallery__card">
        <div class="ui-gallery__card-heading"><span>10</span><div><h2>Rating</h2><p>Keyboard-accessible star response rating</p></div></div>
        <UiRating label="How helpful was this response?" v-model="rating" />
        <p v-if="rating" class="ui-gallery__rating-response" role="status">Thanks for your feedback.</p>
      </article>
    </section>
  </main>
</template>

<script>
import {
  UiButton,
  UiCheckbox,
  UiDatePicker,
  UiIconButton,
  UiRadioGroup,
  UiRating,
  UiSelect,
  UiSwitch,
  UiTextarea,
  UiTextField,
} from './ui';

export default {
  name: 'UiComponentGallery',
  components: {
    UiButton,
    UiCheckbox,
    UiDatePicker,
    UiIconButton,
    UiRadioGroup,
    UiRating,
    UiSelect,
    UiSwitch,
    UiTextarea,
    UiTextField,
  },
  props: {
    palette: {
      type: String,
      default: 'indigo-modern',
    },
    theme: {
      type: String,
      default: 'light',
    },
  },
  data() {
    return {
      activeTheme: this.theme,
      fullName: '',
      search: '',
      details: '',
      topic: '',
      remember: false,
      contactMethod: 'Continue in chat',
      preferredDate: '',
      rating: 0,
      topics: [
        { label: 'General question', value: 'general' },
        { label: 'Technical support', value: 'technical' },
        { label: 'Account assistance', value: 'account' },
        { label: 'Other', value: 'other' },
      ],
      languages: [
        { label: 'English', value: 'en' },
        { label: 'Telugu', value: 'te' },
        { label: 'Hindi', value: 'hi' },
      ],
      contactOptions: [
        'Continue in chat',
        'Fill out a form',
        { label: 'Speak to support', value: 'Speak to support', disabled: true },
      ],
    };
  },
  computed: {
    paletteLabel() {
      return {
        'indigo-modern': 'Indigo Modern',
        'ocean-blue': 'Ocean Blue',
        'modern-sky-blue': 'Modern Sky Blue',
      }[this.palette] || 'Indigo Modern';
    },
    themeLabel() {
      return this.activeTheme === 'dark' ? 'Dark theme' : 'Light theme';
    },
  },
  watch: {
    theme(theme) {
      this.activeTheme = theme;
    },
  },
  methods: {
    changeTheme(isDark) {
      this.activeTheme = isDark ? 'dark' : 'light';
      this.$emit('theme-change', this.activeTheme);
    },
  },
};
</script>
