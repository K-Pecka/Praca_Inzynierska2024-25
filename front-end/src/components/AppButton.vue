<script setup lang="ts">
const props = defineProps<{
  text?: string;
  color?:
    | "primary"
    | "secondary"
    | "accent"
    | "empty"
    | "orange"
    | "red"
    | "primary-outline";
  width?: string;
  maxWidth?: string;
  minHeight?: string;
  icon?: boolean;
  iconName?: string;
  iconSize?: string;
  heightAuto?: boolean | string;
  fontAuto?: boolean | string;
  dense?: boolean | string;
  stretch?: boolean | string;
  disabled?: boolean;
  onClick?: () => any;
}>();
</script>

<template>
  <v-btn
    class="button-media font-weight-bold text-none w-100"
    v-bind="$attrs"
    :disabled="disabled"
    :style="{
      maxWidth: maxWidth || '200px',
      width: width,
      minHeight: minHeight,
    }"
    :class="[
      color,
      heightAuto ? 'height-auto' : '',
      fontAuto ? 'font-auto' : '',
      dense ? 'dense' : '',
      stretch ? 'stretch' : '',
    ]"
    :onClick="onClick"
  >
    <span v-if="text">
      {{ text }}
    </span>
    <v-icon v-if="icon" :size="iconSize || '24px'" :class="{ 'ml-3': text }">
      {{ iconName || "mdi-send" }}
    </v-icon>
  </v-btn>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.dense {
  @media (max-width: 700px) {
    max-width: 100% !important;
  }
}

.primary {
  background: $background-primary;
  border-color: transparent;
  color: white;
}

.primary-outline {
  border: 3px solid $background-primary;
  margin: 3px;
  border-radius: 15px;
  background-color: transparent;
  color: $background-primary;
}

.secondary {
  background-color: rgb($secondary-color);
  color: $text-color;
}

.accent {
  background-color: $accent-color;
  color: white;
}

.orange {
  background-color: #f57f17;
  color: white;
}

.red {
  border: 3px solid #c6564c;
  margin: 3px;
  border-radius: 15px;
  background-color: transparent;
  color: #c6564c;
}

.empty {
  border-width: 2px;
}

.height-auto {
  height: 2.5em;
}

.font-auto {
  font-size: clamp(0.7rem, 0.4vw + 0.4rem, 1.5em);
}

.stretch {
  @media (max-width: 700px) {
    max-width: 1200px !important;
  }
}
</style>
