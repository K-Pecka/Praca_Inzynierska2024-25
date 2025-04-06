<script lang="ts" setup>
import {ref, onMounted, onUnmounted} from "vue";
import {PanelNavbar, SideNav} from "@/components";
import {usePageHomeStore, useUtilStore} from "@/stores";
import { useMockupStore} from "@/mockup/useMockupStore";

const useStore = usePageHomeStore();
const SiteName = useStore.getSiteName();

const {isCurrentRouteNotInSet} = useUtilStore();
const showNavigation = isCurrentRouteNotInSet(["roleSelection", "yourTrip", "TripForm","yourTripGuide"]);

const sideNavOpen = ref(false);

const { getUserInitials } = useMockupStore();
const userInitials = getUserInitials();

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
  <div class="wrapper">
    <v-container fluid class="full-width-container">
      <v-row>
        <v-col cols="12">
          <PanelNavbar :account-icon="userInitials"
                       :show-navigation="showNavigation"
                       @toggleMenu="toggleSideNav">
            <template #logo>
              {{ SiteName }}
            </template>
          </PanelNavbar>
        </v-col>
      </v-row>
      <v-row style="min-height: calc(100vh - 5rem); margin: 0;">
        <v-col
            v-if="showNavigation && (!isMobile || sideNavOpen)"
            cols="12"
            sm="3"
            md="2"
            class="side-nav-col"
            :class="{ 'mobile-overlay': isMobile, 'open': sideNavOpen }"
        >
          <SideNav :mobile="isMobile" @close="toggleSideNav" />
        </v-col>
        <v-col
            :cols="showNavigation ? (isMobile ? 12 : 9) : 12"
            :md="showNavigation ? 10 : 12"
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
  </div>
</template>

<style lang="scss" scoped>
main{
  background-color: rgb(var(--v-theme-background,#F8F9Fa));
}
.wrapper {
  position: relative;
  overflow-x: hidden;
}
@media (max-width: 600px) {
  h1{
    font-size: 2rem;
  }
}
.side-nav-col {
  padding: 0;

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
