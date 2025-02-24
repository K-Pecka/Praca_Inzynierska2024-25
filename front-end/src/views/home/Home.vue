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
  <v-container fluid class="full-width-container">
    <v-row class="sticky-top fixed-center">
      <v-col cols="12" md="10" offset-md="1">
        <v-responsive>
          <Navbar :links="navData">
            <template #logo>
              {{ SiteName }}
            </template>
          </Navbar>
        </v-responsive>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="10" lg="8" offset-lg="2" offset-md="1">
        <main>
          <router-view />
        </main>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <Footer :footerData="footerData">
          <template #logo>
            {{ SiteName }}
          </template>
        </Footer>
      </v-col>
    </v-row>
  </v-container>
</template>
<style lang="scss" scoped>
.v-responsive {
  transition: all 0.3s ease;
}
</style>
