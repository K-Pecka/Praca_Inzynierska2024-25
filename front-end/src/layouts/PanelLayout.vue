<script lang="ts" setup>
import Header from "@/components/panel/Header.vue";
import Navbar from "@/components/panel/Navbar.vue";

defineProps({
  tripId: {
    type: String,
    required: true
  },
  role:{
    type:String,
    required: true
  }
})
</script>

<template>
  <!-- Header -->
  <Header />

  <!-- Navbar -->
  <Navbar />

  <!-- Main Content -->
  <v-col cols="12">
    <router-view class="component-section" />
  </v-col>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.component-section {
  bottom: 0;
  right: 0;
  z-index: 1005;
  overflow-y: auto;
  transform: translateY(0px);
  position: fixed;
  height: calc(100% - $panel-header-height);
  width: calc(100% - $navbar-width);

  @media
  (max-width: 1279px) {
    width: 100%;
  }
}
</style>
