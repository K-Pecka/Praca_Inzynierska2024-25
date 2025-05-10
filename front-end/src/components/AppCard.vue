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
  cols: {
    type: String,
    default: "4",
  },
  bgTransparent: {
    type: Boolean,
    default: false,
  },
  noPadding: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <v-col v-if="!noPadding">
    <v-card
        class="rounded-lg color-text w-100 px-4 pt-1 pb-2"
        :style="style"
        :class="className"
        elevation="4"
    >
      <v-container>
        <slot/>
      </v-container>
    </v-card>
  </v-col>
  <v-card
      class="rounded-lg color-text w-100"
      :style="style"
      :class="className"
      elevation="4"
      v-else
  >
    <v-container>
      <slot/>
    </v-container>
  </v-card>
</template>
<style scoped lang="scss">
.v-card {
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: rgb(var(--v-theme-secondary), 50%);
  height: 100%;
  border-radius: 1.5rem;
}
</style>