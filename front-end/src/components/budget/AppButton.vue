<script setup lang="ts">
defineProps<{
  variant?: "primary" | "secondary" | "accent";
  width?: string;
}>();

</script>

<template>
  <v-btn class="border-none" :style="{ width }" :class="variant">
    <slot/>
  </v-btn>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.primary {
  background-color: $primary-color;
  color: white;
}

.secondary {
  background-color: $secondary-color;
  color: $text-color;
}

.accent {
  background-color: $accent-color;
  color: white;
}

</style>
