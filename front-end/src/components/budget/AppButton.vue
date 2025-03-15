<script setup lang="ts">

defineProps<{ variant?: "primary" | "secondary" }>();
</script>

<template>
  <button class="app-button" :class="variant">
    <slot />
  </button>
</template>

<style scoped lang="scss">
.app-button {
  padding: 8px 40px;
  border-radius: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.primary {
  background-color: rgb(var(--v-theme-primary));
  color: white;
  border: none;
}

.primary:hover {
  background-color: rgba(var(--v-theme-primary), 0.8);
}

.secondary {
  background-color: rgb(var(--v-theme-secondary));
  color: white;
  border: none;
}

.secondary:hover {
  background-color: rgba(var(--v-theme-secondary), 0.8);
}
</style>
