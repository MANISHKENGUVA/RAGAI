<template>
  <div class="ui-field ui-date-picker">
    <label class="ui-field__label" :for="inputId">{{ label }}</label>
    <div class="ui-field__control">
      <input
        :id="inputId"
        class="ui-text-field"
        type="text"
        :value="formattedValue"
        :placeholder="placeholder"
        readonly
        role="combobox"
        aria-haspopup="dialog"
        :aria-expanded="isOpen ? 'true' : 'false'"
        :aria-controls="`${inputId}-calendar`"
        @click="toggleCalendar"
        @keydown.down.prevent="openCalendar"
        @keydown.esc="closeCalendar"
      />
      <button
        class="ui-field__calendar-trigger"
        type="button"
        :aria-label="isOpen ? 'Close date picker' : 'Open date picker'"
        :aria-expanded="isOpen ? 'true' : 'false'"
        @click="toggleCalendar"
      ><span aria-hidden="true">▦</span></button>
    </div>

    <div
      v-if="isOpen"
      :id="`${inputId}-calendar`"
      class="ui-calendar"
      role="dialog"
      :aria-label="label"
      @keydown.esc.stop="closeCalendar"
    >
      <div class="ui-calendar__header">
        <button class="ui-icon-button ui-icon-button--sm" type="button" aria-label="Previous month" title="Previous month" @click="moveMonth(-1)">‹</button>
        <strong>{{ monthLabel }}</strong>
        <button class="ui-icon-button ui-icon-button--sm" type="button" aria-label="Next month" title="Next month" @click="moveMonth(1)">›</button>
      </div>
      <div class="ui-calendar__grid" role="grid" :aria-label="monthLabel">
        <span v-for="weekday in weekdays" :key="weekday" class="ui-calendar__weekday" role="columnheader">{{ weekday }}</span>
        <button
          v-for="day in calendarDays"
          :key="day.iso"
          class="ui-calendar__day"
          :class="{
            'is-outside': !day.inMonth,
            'is-today': day.isToday,
            'is-selected': day.iso === draftValue,
          }"
          type="button"
          role="gridcell"
          :data-date="day.iso"
          :aria-label="day.accessibleLabel"
          :aria-selected="day.iso === draftValue ? 'true' : 'false'"
          :aria-current="day.isToday ? 'date' : null"
          :disabled="day.disabled"
          @click="selectDay(day)"
          @keydown="onDayKeydown($event, day)"
        >{{ day.date }}</button>
      </div>
      <div class="ui-calendar__actions">
        <button class="ui-link-button" type="button" @click="clearDate">Clear date</button>
        <button class="ui-link-button" type="button" @click="selectToday">Today</button>
        <span class="ui-calendar__spacer"></span>
        <button class="ui-button ui-button--secondary ui-button--sm" type="button" @click="closeCalendar">Cancel</button>
        <button class="ui-button ui-button--primary ui-button--sm" type="button" :disabled="!draftValue" @click="applyDate">Apply</button>
      </div>
      <p v-if="error" class="ui-field__error" role="alert">{{ error }}</p>
    </div>
    <span v-if="hint && !error" class="ui-field__hint">{{ hint }}</span>
  </div>
</template>

<script>
let nextDatePickerId = 0;

function toIsoDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function parseIsoDate(value) {
  if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    return null;
  }
  const [year, month, day] = value.split('-').map(Number);
  const date = new Date(year, month - 1, day);
  return date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day
    ? date
    : null;
}

export default {
  name: 'UiDatePicker',
  props: {
    id: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: 'Select date',
    },
    placeholder: {
      type: String,
      default: 'Choose a date',
    },
    value: {
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
    min: {
      type: String,
      default: '',
    },
    max: {
      type: String,
      default: '',
    },
  },
  data() {
    nextDatePickerId += 1;
    const today = new Date();
    return {
      generatedId: `narada-date-${nextDatePickerId}`,
      isOpen: false,
      visibleYear: today.getFullYear(),
      visibleMonth: today.getMonth(),
      draftValue: this.value,
      weekdays: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
    };
  },
  computed: {
    inputId() {
      return this.id || this.generatedId;
    },
    monthLabel() {
      return new Date(this.visibleYear, this.visibleMonth, 1)
        .toLocaleDateString(undefined, { month: 'long', year: 'numeric' });
    },
    formattedValue() {
      const date = parseIsoDate(this.value);
      return date
        ? date.toLocaleDateString(undefined, { day: '2-digit', month: 'short', year: 'numeric' })
        : '';
    },
    calendarDays() {
      const firstWeekday = new Date(this.visibleYear, this.visibleMonth, 1).getDay();
      const start = new Date(this.visibleYear, this.visibleMonth, 1 - firstWeekday);
      const todayIso = toIsoDate(new Date());
      const days = [];

      for (let index = 0; index < 42; index += 1) {
        const date = new Date(start.getFullYear(), start.getMonth(), start.getDate() + index);
        const iso = toIsoDate(date);
        const inMonth = date.getMonth() === this.visibleMonth;
        days.push({
          date: date.getDate(),
          iso,
          inMonth,
          isToday: iso === todayIso,
          disabled: Boolean((this.min && iso < this.min) || (this.max && iso > this.max)),
          accessibleLabel: date.toLocaleDateString(undefined, {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            year: 'numeric',
          }),
        });
      }

      return days;
    },
  },
  watch: {
    value(value) {
      this.draftValue = value;
      const date = parseIsoDate(value);
      if (date) {
        this.visibleYear = date.getFullYear();
        this.visibleMonth = date.getMonth();
      }
    },
  },
  methods: {
    toggleCalendar() {
      if (this.isOpen) {
        this.closeCalendar();
      } else {
        this.openCalendar();
      }
    },
    openCalendar() {
      this.draftValue = this.value;
      const selectedDate = parseIsoDate(this.value) || new Date();
      this.visibleYear = selectedDate.getFullYear();
      this.visibleMonth = selectedDate.getMonth();
      this.isOpen = true;
      this.$nextTick(() => {
        const focusDate = this.draftValue || toIsoDate(new Date());
        const button = this.$el.querySelector(`[data-date="${focusDate}"]:not(:disabled)`);
        if (button) {
          button.focus();
        }
      });
    },
    closeCalendar() {
      this.isOpen = false;
    },
    moveMonth(offset) {
      const nextMonth = new Date(this.visibleYear, this.visibleMonth + offset, 1);
      this.visibleYear = nextMonth.getFullYear();
      this.visibleMonth = nextMonth.getMonth();
    },
    selectDay(day) {
      if (!day.disabled) {
        this.draftValue = day.iso;
      }
    },
    selectToday() {
      const today = new Date();
      const iso = toIsoDate(today);
      if (!((this.min && iso < this.min) || (this.max && iso > this.max))) {
        this.visibleYear = today.getFullYear();
        this.visibleMonth = today.getMonth();
        this.draftValue = iso;
      }
    },
    clearDate() {
      this.draftValue = '';
      this.$emit('input', '');
      this.closeCalendar();
    },
    applyDate() {
      if (this.draftValue) {
        this.$emit('input', this.draftValue);
        this.closeCalendar();
      }
    },
    onDayKeydown(event, day) {
      const offsets = {
        ArrowLeft: -1,
        ArrowRight: 1,
        ArrowUp: -7,
        ArrowDown: 7,
      };
      const offset = offsets[event.key];
      if (!offset) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          this.selectDay(day);
        }
        return;
      }

      event.preventDefault();
      const target = new Date(
        Number(day.iso.slice(0, 4)),
        Number(day.iso.slice(5, 7)) - 1,
        Number(day.iso.slice(8, 10)) + offset,
      );
      const targetIso = toIsoDate(target);
      this.visibleYear = target.getFullYear();
      this.visibleMonth = target.getMonth();
      this.$nextTick(() => {
        const button = this.$el.querySelector(`[data-date="${targetIso}"]:not(:disabled)`);
        if (button) {
          button.focus();
        }
      });
    },
  },
};
</script>
