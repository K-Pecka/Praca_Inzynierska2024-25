<script setup lang="ts">

defineProps<{ variant?: "primary" | "secondary", size?: "sm" | "md" | "lg" }>();
</script>

<template>
  <v-btn class="app-button" :class="variant, size">
    <slot/>
  </v-btn>
</template>

<style scoped lang="scss">
.app-button {
  border-radius: 5px;
  font-weight: bold;
  width: fit-content;
  text-transform: none;
}

.sm {
  padding: 6px 20px;
  font-size: 0.8rem;
}

.md {
  padding: 8px 32px;
  font-size: 1rem;
}

.lg {
  padding: 12px 48px;
  font-size: 1.2rem;
}

.primary {
  background-color: rgb(var(--v-theme-primary));
  color: white;
  border: none;
}

.primary:hover {
  background-color: rgba(var(--v-theme-primary),1);
}

.secondary {
  background-color: rgb(var(--v-theme-secondary));
  color: rgba(var(--v-theme-text), 0.8);
  border: none;
}

.secondary:hover {
  background-color: rgba(var(--v-theme-secondary), 0.8);
}
</style>
