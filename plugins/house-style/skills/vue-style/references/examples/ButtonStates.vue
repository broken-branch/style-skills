<!-- [VUE-STYLE] keyed loop; [VUE-REACTIVITY] local ref; [WCAG22] native button states. Neutral tokens begin the scoped style block. -->
<script setup lang="ts">
import { ref } from 'vue';

const previews = ['default', 'hover', 'focus-visible', 'active'] as const;
const activations = ref(0);
</script>

<template>
  <div class="demo-panel">
    <p>
      Hover, press or Tab to a button. Named previews illustrate each state.
    </p>
    <div class="demo-row">
      <button
        v-for="preview in previews"
        :key="preview"
        class="demo-button"
        type="button"
        :data-preview="preview"
        @click="activations += 1"
      >
        {{ preview }}
      </button>
      <button class="demo-button" type="button" disabled>Disabled</button>
      <button class="demo-button" type="button" disabled aria-busy="true">
        Loading…
      </button>
    </div>
    <p role="status">Activated {{ activations }} times.</p>
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
</style>
