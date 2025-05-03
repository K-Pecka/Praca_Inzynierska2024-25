<script setup lang="ts">
import Header from "@/components/panel/Header.vue";
</script>

<template>
  <Header/>

  <v-container>
    <v-col cols="12">
      <v-row class="flex-column align-center">
        <router-view />
      </v-row>
    </v-col>
  </v-container>
</template>

<style scoped lang="scss">

</style>