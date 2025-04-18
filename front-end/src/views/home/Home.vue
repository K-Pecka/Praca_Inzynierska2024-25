<script lang="ts" setup>
import { computed } from "vue";
import { Navbar, Footer } from "@/components/home";
import { usePageHomeStore } from "@/stores";

const useStore = usePageHomeStore();
const SiteName = computed(() => useStore.getSiteName());
const navData = computed(() => useStore.navigationLinks);
const footerData = computed(() => useStore.getFooterData());
</script>

<template>
  <v-container class="full-width-container">
    <v-row class="sticky-top fixed-center">
      <v-col cols="12" sm="12" lg="12" offset-lg="0" offset-sm="0">
        <Navbar :links="navData">
          <template #logo>
              <img
                src="/picture/logo.svg"
                :alt="SiteName"
                lazy-src="/images/placeholder.jpg"
              />
          </template>
        </Navbar>
      </v-col>
    </v-row>

    <v-row class="d-flex justify-center">
      <v-col cols="12">
        <main>
          <router-view />
        </main>
      </v-col>
    </v-row>
  </v-container>

  <Footer :footerData="footerData">
    <template #logo>
      <img
          src="/picture/logo.svg"
          :alt="SiteName"
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
  min-height: 50vh;
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
