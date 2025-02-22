<script lang="ts" setup>
import Navbar from "@/components/home/Navbar.vue";
import Footer from "@/components/home/Footer.vue";
import { usePageHomeStore } from '@/stores/';
const useStore = usePageHomeStore();

const SiteName = useStore.getSiteName();
const navData = useStore.navigationLinks;
const footerData = useStore.getFooterData();
console.log(footerData);
</script>

<template>
  <v-app>
    <v-container fluid class="full-width-container">
      <v-row class="sticky-top fixed-center">
        <v-col cols="12" md="10" offset-md="1">
          <Navbar :links="navData">
            <template #logo>
              {{ SiteName }}
            </template>
          </Navbar>
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
  </v-app>
</template>
<style lang="scss" scoped>

.v-application{
  background-color: rgba(var(--v-theme-background),0.1);
}
* //TODO: przetestować brak tego zapisu
{
  transition: all 0.3s ease;
}
</style>