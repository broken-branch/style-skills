<!-- [VUE-PROPS] reactive typed props; [VUE-LINT] typed emit; [VUE-TEMPLATE-REFS] nullable DOM refs; [WCAG22] modal focus. Neutral tokens begin the scoped style block. -->
<script setup lang="ts">
import { ref, useId, useTemplateRef } from 'vue';

interface Props {
  /** Visible question used as the dialog's accessible name. */
  readonly question?: string;
}

const { question = 'Use the compact view?' } = defineProps<Props>();
const emit = defineEmits<{ viewSelected: [view: 'compact'] }>();
const titleId = useId();
const dialog = useTemplateRef<HTMLDialogElement>('dialog');
const opener = useTemplateRef<HTMLButtonElement>('opener');
const cancel = useTemplateRef<HTMLButtonElement>('cancel');
const apply = useTemplateRef<HTMLButtonElement>('apply');
const notice = ref('');

function handleOpen() {
  dialog.value?.showModal();
  cancel.value?.focus();
}

function handleApply() {
  notice.value = 'Compact view selected.';
  dialog.value?.close();
  emit('viewSelected', 'compact');
}

function handleKeyDown(event: KeyboardEvent) {
  if (event.key !== 'Tab') return;
  // The two controls are always mounted and enabled, so no DOM patch is pending.
  // Dynamic dialog content needs its current Tab order after nextTick instead.
  const boundary = event.shiftKey ? cancel.value : apply.value;
  if (dialog.value?.ownerDocument.activeElement === boundary) {
    event.preventDefault();
    (event.shiftKey ? apply.value : cancel.value)?.focus();
  }
}
</script>

<template>
  <div class="demo-panel">
    <button ref="opener" class="demo-button" type="button" @click="handleOpen">
      Open view chooser
    </button>
    <dialog
      ref="dialog"
      class="demo-dialog"
      :aria-labelledby="titleId"
      @keydown="handleKeyDown"
      @close="opener?.focus()"
    >
      <h2 :id="titleId">{{ question }}</h2>
      <p>This example changes only the status below.</p>
      <div class="demo-row">
        <button
          ref="cancel"
          class="demo-button"
          type="button"
          @click="dialog?.close()"
        >
          Cancel
        </button>
        <button
          ref="apply"
          class="demo-button"
          type="button"
          @click="handleApply"
        >
          Apply view
        </button>
      </div>
    </dialog>
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
.demo-dialog {
  box-sizing: border-box;
  max-inline-size: min(28rem, calc(100% - 2rem));
  max-block-size: calc(100% - 2rem);
  overflow: auto;
  padding: 1.5rem;
  border: 1px solid var(--demo-edge);
  border-radius: var(--demo-radius);
  color: var(--demo-ink);
  background: var(--demo-paper);
}
.demo-dialog::backdrop {
  background: rgb(0 0 0 / 45%);
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
