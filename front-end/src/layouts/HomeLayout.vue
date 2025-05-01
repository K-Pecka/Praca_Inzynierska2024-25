<script lang="ts" setup>
import { computed } from "vue";
import { HomeHeader, Footer } from "@/components/home";
import { usePageHomeStore } from "@/stores";
import { images } from "@/data";

const useStore = usePageHomeStore();
const SiteName = computed(() => useStore.getSiteName());
const navData = computed(() => useStore.navigationLinks);
const footerData = computed(() => useStore.getFooterData());
</script>

<template>

  <HomeHeader :links="navData" />
  <v-col cols="12" class="d-flex flex-column align-center">
    <main class="d-flex flex-column align-center">
      <router-view />
    </main>
  </v-col>


  <Footer :footerData="footerData">
    <template #logo>
      <img
          :src="images.logo.img"
          :alt="images.logo.alt"
          lazy-src="/images/placeholder.jpg"
        />
    </template>
  </Footer>
</template>
<style lang="scss" scoped>

.v-container {
  position: relative;
  z-index: 2;
}
.wrapper {
  position: relative;
  overflow-x: hidden;
}
main {
  width: 90%;
}
.wrapper::after {
  content: "";
  display: none;
  width: 50%;
  height: 50%;
  border-radius: 50%;
  background-color: rgb(var(--v-theme-secondary));
  position: absolute;
  top: -7vw;
  right: -6vw;
  z-index: 1;
}
</style>
