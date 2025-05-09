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
    <main class="d-flex flex-column align-center main-style">
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

.main-style {
  margin-top: 8rem;
}

main {
  width: 90%;
}

</style>
