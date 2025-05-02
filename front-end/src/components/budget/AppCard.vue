<script setup lang="ts">
defineProps({
  className: {
    type: String,
    default: "",
  },
  style: {
    type: Object,
    default: () => ({}),
  },
  elevation: {
    type: Number,
    default: 1,
  },
});
</script>

<template>
  <v-card class="pa-4 my-3 rounded-lg" :style="style" :class="className" :elevation="elevation">
    <slot />
  </v-card>
</template>
