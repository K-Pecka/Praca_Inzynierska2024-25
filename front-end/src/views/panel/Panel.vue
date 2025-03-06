<script lang="ts" setup>
import {ref, onMounted, onUnmounted} from "vue";
import {PanelNavbar, SideNav} from "@/components";
import {usePageHomeStore, usePagePanelStore, useUtilStore} from "@/stores";

const useStore = usePageHomeStore();
const SiteName = useStore.getSiteName();

const {navbar, getSideNavItems} = usePagePanelStore();
const {isCurrentRouteNotInSet, getTripId} = useUtilStore();
const sideNavItems = getSideNavItems(getTripId("tripId").value as string);
const showNavigation = isCurrentRouteNotInSet(["roleSelection", "yourTrip", "TripForm"]);

const sideNavOpen = ref(false);

function toggleSideNav() {
  sideNavOpen.value = !sideNavOpen.value;
}

const isMobile = ref(window.innerWidth <= 1000);

function updateScreenSize() {
  isMobile.value = window.innerWidth <= 1000;
}

onMounted(() => {
  window.addEventListener("resize", updateScreenSize);
});

onUnmounted(() => {
  window.removeEventListener("resize", updateScreenSize);
});
</script>

<template>
  <v-app>
    <v-container fluid class="full-width-container">
      <v-row style="height: 5rem; margin: 0">
        <v-col>
          <PanelNavbar :account-icon="navbar.accountIcon"
                       @toggleMenu="toggleSideNav">
            <template #logo>
              {{ SiteName }}
            </template>
          </PanelNavbar>
        </v-col>
      </v-row>
      <v-row style="height: calc(100vh - 5rem); margin: 0; position: relative;">
        <v-col
            v-if="showNavigation && (!isMobile || sideNavOpen)"
            cols="12"
            sm="3"
            md="2"
            class="side-nav-col"
            :class="{ 'mobile-overlay': isMobile, 'open': sideNavOpen }"
        >
          <SideNav :items="sideNavItems" :mobile="isMobile" @close="toggleSideNav" />
        </v-col>
        <v-col
            :cols="showNavigation ? 9 : 12"
            :md="showNavigation ? 10 : 12"
            class="full-height"
        >
          <main>
            <router-view/>
          </main>
        </v-col>
        <div
            v-if="sideNavOpen && isMobile"
            class="overlay"
            @click="toggleSideNav"
        />
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

main {
  height: 100%;
}

.mobile-overlay {
  position: fixed;
  top: 5rem;
  left: 0;
  height: calc(100vh - 5rem);
  width: 70%;
  max-width: 280px;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 1500;

  &.open {
    transform: translateX(0);
  }
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1400;
}
</style>
