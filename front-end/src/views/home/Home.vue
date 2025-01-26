<script lang="ts" setup>
import Navbar from "@/components/home/Navbar.vue";
import Footer from "@/components/home/Footer.vue";
import { usePageStore } from '@/stores/pageContentStore';
const useStore = usePageStore();

const SiteName = useStore.SiteName();

const navData = useStore.navLinks();
const footerData = useStore.footerData();
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
*
{
  transition: all 0.3s ease;
}
</style>