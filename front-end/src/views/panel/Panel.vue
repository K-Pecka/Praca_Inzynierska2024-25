<script lang="ts" setup>
import {ref, computed} from "vue";
import PanelNavbar from "@/components/trip/PanelNavbar.vue";
import SideNav from "@/components/trip/SideNav.vue";
import {usePageHomeStore} from "@/stores/ui/usePageHomeStore";
import {usePagePanelStore} from "@/stores/panelContentStore";
import { useRoute } from "vue-router";

const useStore = usePageHomeStore();
const SiteName = useStore.getSiteName()

const panelContentStore = usePagePanelStore();

const {navbar, getsideNavItems} = panelContentStore;
const route = useRoute();
const sideNavItems = getsideNavItems(route.params.tripId as string);
const form = ref({
  email: "",
  password: "",
});
const hiddenNavRoutes = ["roleSelection", "yourTrip","TripForm"];
const showNavigation = computed(() => {
  return !hiddenNavRoutes.includes(route.name as string);
});
</script>
<template>
  <v-app>
    <v-container fluid class="full-width-container">
    <v-row>
      <v-col>
        <PanelNavbar :account-icon="navbar.accountIcon" >
          <template #logo>
            {{ SiteName }}
          </template>
        </PanelNavbar>
      </v-col>
    </v-row>
      <v-row style="height: calc(100vh - 64px); margin: 0;">
        <v-col v-if="showNavigation" cols="12" sm="3" md="2" class="side-nav-col">
          <SideNav :items="sideNavItems" class="full-height" />
        </v-col>
        <v-col :cols="showNavigation ? 9 : 12" :md="showNavigation ? 10 : 12" class="full-height">
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
main{
  height: 90%;
}


</style>