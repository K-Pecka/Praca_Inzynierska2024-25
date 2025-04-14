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
  elevation: {
    type: Number,
    default: 1,
  },
});
</script>

<template>
  <v-card class="pa-4 my-3 rounded-lg" :style="style" :class="className" :elevation="elevation">
    <slot />
  </v-card>
</template>

<style scoped>
.v-card {
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: rgb(var(--v-theme-secondary), 50%);
  height: 100%;
  border-radius: 1.5rem;
}
.backgroud-card{
  background-color: rgb(var(--v-theme-background));
}
 /*.v-card:hover {
 transform: translateY(-3px);
}*/
</style>
