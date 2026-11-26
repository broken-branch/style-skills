<!-- Vue Style Guide: [avoid-v-if-with-v-for] computed filtering;
     [use-keyed-v-for] stable IDs; [component-instance-options-order] Options API.
     entries are { id: string, title: string, finished: boolean } records. -->
<script>
import ReadingQueueItem from './ReadingQueueItem.vue';

export default {
  name: 'ReadingQueue',

  components: { ReadingQueueItem },

  props: {
    entries: {
      type: Array,
      required: true,
      validator: (entries) => entries.every((entry) =>
        entry !== null && typeof entry === 'object' &&
        typeof entry.id === 'string' && typeof entry.title === 'string' &&
        typeof entry.finished === 'boolean'
      ) && new Set(entries.map((entry) => entry.id)).size === entries.length,
    },
  },

  emits: ['finish'],

  computed: {
    unfinishedEntries() {
      return this.entries.filter((entry) => !entry.finished);
    },
  },
};
</script>

<template>
  <ul v-if="unfinishedEntries.length">
    <ReadingQueueItem
      v-for="entry in unfinishedEntries"
      :key="entry.id"
      :entry-id="entry.id"
      :title="entry.title"
      @finish="$emit('finish', $event)"
    />
  </ul>
  <p v-else>Nothing left to read.</p>
</template>
