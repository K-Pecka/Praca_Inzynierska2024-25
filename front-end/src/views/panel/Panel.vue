<script lang="ts" setup>
import {ref, onMounted, onUnmounted} from "vue";
import {PanelNavbar, SideNav} from "@/components";
import {usePageHomeStore, useUtilsStore, useAuthStore} from "@/stores";
import { images } from "@/data";

const useStore = usePageHomeStore();
const SiteName = useStore.getSiteName();

const logoText = ref(SiteName);

const authStore = useAuthStore();

const userInitials = authStore.getUserInitials();

const {isCurrentRouteNotInSet} = useUtilsStore();
const showNavigation = isCurrentRouteNotInSet([
  "roleSelection",
  "yourTrip",
  "TripForm",
  "yourTripGuide",
]);

const sideNavOpen = ref(false);

function toggleSideNav() {
  sideNavOpen.value = !sideNavOpen.value;
}

const isMobile = ref(window.innerWidth <= 959);

function updateScreenSize() {
  isMobile.value = window.innerWidth <= 959;
  logoText.value = window.innerWidth <= 425 ? "P" : SiteName;
}

onMounted(() => {
  window.addEventListener("resize", updateScreenSize);
  document.documentElement.style.overflowY = 'hidden';
})
onUnmounted(() => {
  window.removeEventListener("resize", updateScreenSize);
  document.documentElement.style.overflowY = 'scroll';
});
</script>

<template>
  <v-row>
    <v-col cols="12">
      <PanelNavbar
          :account-icon="userInitials"
          :show-navigation="showNavigation"
          @toggleMenu="toggleSideNav"
      >
        <template #logo>
          <img
            :src="images.logo.img"
            :alt="images.logo.alt"
          />
        </template>
      </PanelNavbar>
    </v-col>
  </v-row>
  <v-row style="min-height: calc(100vh - 5rem); margin: 0">
    <transition name="slide-nav">
      <v-col
          v-if="showNavigation && (!isMobile || sideNavOpen)"
          cols="2"
          class="side-nav-col"
          :class="{ 'mobile-overlay': isMobile, open: sideNavOpen }"
      >
        <SideNav :mobile="isMobile" @close="toggleSideNav"/>
      </v-col>
    </transition>
    <v-col
        :cols="showNavigation ? (isMobile ? 12 : 10) : 12"
        :md="showNavigation ? 10 : 12"
        class="main-col"
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
</template>

<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

main {
  background-color: rgb(var(--v-theme-background));
  height: 100%;
  max-height: calc(100vh - 5rem);
  overflow-y: auto;
}

.wrapper {
  position: relative;
  overflow-x: hidden;
}

@media (max-width: 600px) {
  h1 {
    font-size: 2rem;
  }
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1400;
}

.side-nav-col {
  padding: 0;


  @media (min-width: 959px) {
    position: relative;
    z-index: auto;
  }

  @media (max-width: 959px) {
    position: fixed;
    top: 5rem;
    left: 0;
    bottom: 0;
    width: 300px;
    z-index: 1500;
    overflow-y: auto;
  }

}

.slide-nav-enter-active,
.slide-nav-leave-active {
  transition: transform 0.4s ease, opacity 0.4s ease;
}

.slide-nav-enter-from,
.slide-nav-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-nav-enter-to,
.slide-nav-leave-from {
  transform: translateX(0);
  opacity: 1;
}

.main-col {
  height: calc(100vh - 5rem);
  overflow: hidden;
  padding: 0;
}
</style>
