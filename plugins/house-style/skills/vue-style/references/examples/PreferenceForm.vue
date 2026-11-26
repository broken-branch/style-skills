<!-- [VUE-SFC] typed script setup; [VUE-REACTIVITY] pure computed error; [VUE-TEMPLATE-REFS] nullable handle; [WCAG22] labels and switch. Neutral tokens begin the scoped style block. -->
<script setup lang="ts">
import { computed, ref, useId, useTemplateRef } from 'vue';

const id = useId();
const titleInput = useTemplateRef<HTMLInputElement>('title-input');
const title = ref('');
const compact = ref(false);
const submitted = ref(false);
const notice = ref('');
const invalid = computed(() => submitted.value && title.value.trim() === '');

function handleSubmit() {
  submitted.value = true;
  if (invalid.value) {
    notice.value = 'Preferences need a title.';
    titleInput.value?.focus();
    return;
  }
  notice.value = 'Preferences previewed. Nothing was saved.';
}
</script>

<template>
  <div class="demo-panel">
    <form novalidate @submit.prevent="handleSubmit">
      <div class="demo-field">
        <label :for="`${id}-title`">Item title (required)</label>
        <input
          :id="`${id}-title`"
          ref="title-input"
          v-model="title"
          class="demo-input"
          name="title"
          type="text"
          required
          :aria-invalid="invalid"
          :aria-describedby="`${id}-error`"
          @input="notice = ''"
        />
        <p :id="`${id}-error`" class="demo-error">
          {{ invalid ? 'Error: enter an item title.' : '' }}
        </p>
      </div>
      <label class="demo-switch">
        <input v-model="compact" type="checkbox" role="switch" name="compact" />
        Compact layout
      </label>
      <button class="demo-button" type="submit">Preview preferences</button>
    </form>
    <p role="status">{{ notice }}</p>
  </div>
</template>

<style scoped>
.demo-panel {
  --demo-ink: #222;
  --demo-paper: #fff;
  --demo-edge: #666;
  --demo-hover: #eee;
  --demo-pressed: #ddd;
  --demo-gap: 0.75rem;
  --demo-radius: 0.25rem;
  color: var(--demo-ink);
  background: var(--demo-paper);
  font-family: system-ui, sans-serif;
  line-height: 1.5;
  padding: 1rem;
  overflow-wrap: anywhere;
}
.demo-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--demo-gap);
  align-items: center;
}
.demo-button {
  min-block-size: 2.75rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--demo-edge);
  border-radius: var(--demo-radius);
  color: var(--demo-ink);
  background: var(--demo-paper);
  font: inherit;
  cursor: pointer;
}
.demo-button:where(:hover, [data-preview='hover']):not(:disabled) {
  background: var(--demo-hover);
}
.demo-button:where(:focus-visible, [data-preview='focus-visible']) {
  outline: 2px solid currentcolor;
  outline-offset: 3px;
}
.demo-button:where(:active, [data-preview='active']):not(:disabled) {
  background: var(--demo-pressed);
  border-color: currentcolor;
}
.demo-button:disabled {
  cursor: not-allowed;
  border-style: dashed;
}
.demo-button[aria-busy='true'] {
  cursor: progress;
}
@media (forced-colors: active) {
  .demo-button:where(:focus-visible, [data-preview='focus-visible']) {
    outline-color: Highlight;
  }
}
.demo-field {
  display: grid;
  gap: var(--demo-gap);
}
.demo-input {
  box-sizing: border-box;
  max-inline-size: 100%;
  min-inline-size: 0;
  min-block-size: 2.75rem;
  padding: 0.5rem;
  color: var(--demo-ink);
  background: var(--demo-paper);
  border: 1px solid var(--demo-edge);
  border-radius: var(--demo-radius);
  font: inherit;
}
.demo-input[aria-invalid='true'] {
  border-width: 2px;
}
.demo-error {
  font-weight: 700;
}
.demo-switch {
  display: flex;
  align-items: center;
  gap: var(--demo-gap);
  min-block-size: 2.75rem;
}
.demo-switch input {
  inline-size: 1.5rem;
  block-size: 1.5rem;
  accent-color: var(--demo-ink);
}
:where(.demo-input, .demo-switch input):focus-visible {
  outline: 2px solid currentcolor;
  outline-offset: 3px;
}
@media (forced-colors: active) {
  :where(.demo-input, .demo-switch input):focus-visible {
    outline-color: Highlight;
  }
}
</style>
