<script lang="ts" setup>
import {ref} from "vue";
import PanelNavbar from "@/components/trip/PanelNavbar.vue";
import {usePageStore} from "@/stores/pageContentStore";
import {usePanelContentStore} from "@/stores/panelContentStore";

const useStore = usePageStore();
const SiteName = useStore.SiteName()

const panelContentStore = usePanelContentStore();

const {navbar} = panelContentStore;

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
      <v-row>
<!--        <v-col>
        </v-col>-->
        <v-col>
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
</style>