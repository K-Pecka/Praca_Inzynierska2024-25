<template>
  <v-row
    class="fill-height"
    align="center"
    justify="center"
  >
    <v-col class="text-center">
      <v-progress-circular indeterminate color="primary" size="32" />
      <div v-if="text" class="mt-2 text-caption">{{ text }}</div>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
defineProps<{ text?: string }>();
</script>
