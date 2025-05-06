<script setup lang="ts">
defineProps<{
  text?: string;
  variant?: "primary" | "secondary" | "accent";
  width?: string;
  maxWidth?: string;
  heightAuto?: boolean | string;
  fontAuto?: boolean | string;
  dense?: boolean | string;
  stretch?: boolean | string;
  onClick?: () => any
}>();

</script>

<template>
  <v-btn
      class="button-media border-none font-weight-bold text-none w-100"
      v-bind="$attrs"
      :style="{ maxWidth: maxWidth ? width : '200px', width: width }"
      :class="[
       variant,
       heightAuto ? 'height-auto' : '',
       fontAuto ? 'font-auto' : '',
       dense ? 'dense' : '',
       stretch ? 'stretch' : ''
      ]"
      :onClick = onClick
  >
    {{text}}
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
  background-color: $primary-color;
  color: white;
}

.secondary {
  background-color: $secondary-color;
  color: $text-color;
}

.accent {
  background-color: rgb($accent-color);
  color: white;
}

.height-auto {
  height: 2.5em;
}

.font-auto {
  font-size: clamp(1em, 0.4vw + 0.4rem, 1.5em);
}

.stretch {
  @media(max-width: 700px) {
    max-width: 1200px !important;
  }
}

</style>
