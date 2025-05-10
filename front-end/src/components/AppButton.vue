<script setup lang="ts">
defineProps<{
  text?: string;
  color?: "primary" | "secondary" | "accent" | "empty" | "orange" | "red";
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
  onClick?: () => any
}>();

</script>

<template>
  <v-btn
      class="button-media font-weight-bold text-none w-100"
      v-bind="$attrs"
      :style="{
        maxWidth: maxWidth || '200px',
        width: width,
        minHeight: minHeight
      }"
      :class="[
       color,
       heightAuto ? 'height-auto' : '',
       fontAuto ? 'font-auto' : '',
       dense ? 'dense' : '',
       stretch ? 'stretch' : ''
      ]"
      :onClick = onClick
  >
    <span v-if="text">
      {{text}}
    </span>
    <v-icon
        v-if="icon"
        :size="iconSize || '24px'"
        :class="{ 'ml-3': text }"
    >
      {{ iconName || 'mdi-send'}}
    </v-icon>
  </v-btn>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.dense {
  @media(max-width: 700px) {
    max-width: 100% !important;
  }
}

.primary {
  background: $background-primary;
  color: white;
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
  background-color: #F57F17;
  color: white;
}

.red {
  background-color: #c6564c;
  color: white;
}

.empty {
  border-width: 2px;
}

.height-auto {
  height: 2.5em;
}

.font-auto {
  font-size: clamp(0.5em, 0.4vw + 0.4rem, 1.5em);
}

.stretch {
  @media(max-width: 700px) {
    max-width: 1200px !important;
  }
}

</style>
