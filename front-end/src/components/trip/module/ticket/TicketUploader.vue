<script setup lang="ts">
import { ref } from "vue";

const ticketFile = ref<File | null>(null);

</script>

<template>
  <v-file-input
      class="custom-file-uploader"
      label="Przeciągnij lub dodaj bilet"
      accept="image/*, application/pdf"
      prepend-icon="mdi-upload"
      v-model="ticketFile"
      show-size
      outlined
  />
</template>

<style scoped lang="scss">

</style>