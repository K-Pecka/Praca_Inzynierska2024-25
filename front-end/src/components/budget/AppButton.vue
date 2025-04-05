<script setup lang="ts">

defineProps<{ variant?: "primary" | "secondary", size?: "sm" | "md" | "lg" }>();
</script>

<template>
  <v-btn clbuttonass="app-button" :class="variant, size">
    <slot/>
  </v-btn>
</template>

<style scoped lang="scss">
.app-button {
  padding: 8px 40px;
  border-radius: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  width: fit-content;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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
