<script setup lang="ts">

</script>

<template>
  <v-card class="app-card">
    <slot />
  </v-card>
</template>

<style scoped>
.app-card {
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

</style>
