<script setup lang="ts">
import { defineProps } from "vue";

defineProps<{ variant?: "primary" | "secondary" }>();
</script>

<template>
  <button class="app-button" :class="variant">
    <slot />
  </button>
</template>

<style scoped>
.app-button {
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.primary {
  background-color: #4a90e2;
  color: white;
  border: none;
}

.primary:hover {
  background-color: #357abd;
}

.secondary {
  background-color: transparent;
  color: #4a90e2;
  border: 2px solid #4a90e2;
}

.secondary:hover {
  background-color: #4a90e2;
  color: white;
}
</style>
