<script lang="ts" setup>
import {ref} from "vue";
import PanelNavbar from "@/components/trip/PanelNavbar.vue";
import SideNav from "@/components/trip/SideNav.vue";
import {usePageStore} from "@/stores/pageContentStore";
import {usePanelContentStore} from "@/stores/panelContentStore";


const useStore = usePageStore();
const SiteName = useStore.SiteName()

const panelContentStore = usePanelContentStore();

const {navbar, sideNavItems} = panelContentStore;

const form = ref({
  email: "",
  password: "",
});
</script>
<template>
  <v-app>
    <v-container fluid class="full-width-container">
    <v-row>
      <v-col>
        <PanelNavbar :account-icon="navbar.accountIcon">
          <template #logo>
            {{ SiteName }}
          </template>
        </PanelNavbar>
      </v-col>
    </v-row>
      <v-row style="height: calc(100vh - 64px); margin: 0;">
        <v-col cols="12" sm="3" md="2" class="side-nav-col">
          <SideNav :items="sideNavItems" class="full-height" />
        </v-col>
        <v-col cols="12" sm="9" md="10" class="full-height">
          <main>
          <router-view/>
          </main>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<style lang="scss" scoped>
* {
  transition: all 0.3s ease;
}

.side-nav-col {
  padding: 0;
}
.full-height {
  height: 100%;
  overflow: auto;
}



</style>