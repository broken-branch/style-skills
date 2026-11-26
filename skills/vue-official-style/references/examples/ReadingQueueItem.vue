<!-- Vue Style Guide: [tightly-coupled-component-names] parent prefix;
     [use-detailed-prop-definitions] typed props;
     [implicit-parent-child-communication] emit instead of mutating props;
     [element-selectors-with-scoped] scoped class selector. -->
<script>
export default {
  name: 'ReadingQueueItem',

  props: {
    entryId: { type: String, required: true },
    title: { type: String, required: true },
  },

  emits: {
    finish: (entryId) => typeof entryId === 'string',
  },
};
</script>

<template>
  <li class="reading-queue-item">
    <span>{{ title }}</span>
    <button
      type="button"
      :aria-label="`Mark ${title} as finished`"
      @click="$emit('finish', entryId)"
    >
      Finish
    </button>
  </li>
</template>

<style scoped>
.reading-queue-item {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.5rem;
}
</style>
