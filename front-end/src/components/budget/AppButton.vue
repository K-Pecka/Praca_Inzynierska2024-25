<script setup lang="ts">
defineProps<{
  variant?: "primary" | "secondary" | "accent";
  width?: string;
  height?: string;
  fontSize?: string;
}>();

</script>

<template>
  <v-btn
      class="border-none font-weight-bold text-none w-100"
      v-bind="$attrs"
      :style="{ maxWidth: width }"
      :class="[variant, height, fontSize]"
  >
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

.height-auto {
  height: 2.5em;
}

.font-auto {
  font-size: clamp(0.4em, 0.4vw + 0.4rem, 1em);
}

</style>
