<script lang="ts" setup>
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
    default: () => ({}),
  },
});
</script>
<template>
  <v-card :style="style" :class="className" :elevation="elevation">
    <v-card-title class="text-h6 font-weight-medium d-flex align-center">
        <v-icon class="mr-2" color="primary"><slot name="titleIcon"> </slot></v-icon>
        <slot name="title"> </slot>
    </v-card-title>
    <v-card-text>
        <slot name="content"> </slot>
    </v-card-text>
  </v-card>
</template>
<style scoped>
.v-card {
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: rgb(var(--v-theme-secondary), 50%);
  height: 100%;
  border-radius: 1.5rem;
}
.v-card-title {
  font-size: 20px;
  font-weight: bold;
  font-family: var(--v-fontFamily);
  padding-bottom: 2rem;
}
.v-card-text {
  font-size: 20px;
  font-family: var(--v-fontFamily);
}
.v-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}
</style>