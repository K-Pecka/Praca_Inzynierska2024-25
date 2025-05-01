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
    default: 1,
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

</style>