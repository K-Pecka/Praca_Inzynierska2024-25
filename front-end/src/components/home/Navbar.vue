<script lang="ts" setup>
import { ref } from "vue";
import { Link } from "@/type";

defineProps<{ links: Link[] }>();

const menuOpen = ref(false);

const toggleMenu = (mode?: boolean) => {
  const currentMode = mode ?? !menuOpen.value;
  document.documentElement.style.overflow = currentMode ? "hidden" : "auto";
  menuOpen.value = currentMode;
};

import { watch } from "vue";
import { useDisplay } from "vuetify";

const { smAndDown } = useDisplay();

watch(smAndDown, (isSmallScreen) => {
  if (!isSmallScreen) {
    menuOpen.value = false;
    document.documentElement.style.overflow = "auto";
  }
});
</script>

<template>
  <nav class="navbar">
    <div class="navbar__container">
      <router-link to="/" class="navbar__logo">
        <slot name="logo">
          <h1>Logo</h1>
        </slot>
      </router-link>

      <v-icon class="navbar__hamburger" icon="mdi-menu" @click="() => toggleMenu(true)" />

      <ul class="navbar__links" :class="{ open: menuOpen }">
        <li
          v-for="(link, index) in links"
          :key="index"
          class="navbar__item"
          :class="[
            ...(Array.isArray(link.className)
              ? link.className
              : link.className
              ? [link.className]
              : [])
          ]"
        >
          <router-link
            :to="link.href"
            class="navbar__link"
            :class="{ 'navbar__link--active': link.active }"
            :style="link.style"
          >
            {{ link.label }}
          </router-link>
        </li>
      </ul>

      <Teleport to="body">
        <div v-if="menuOpen" class="navbar__backdrop" @click="() => toggleMenu(false)">
          <transition name="slide-menu">
            <div class="navbar__sidebar slide-menu mobile" :class="{ open: menuOpen }">
              <div class="navbar__close" @click="() => toggleMenu(false)">
                <v-icon>mdi-close</v-icon>
              </div>
              <div class="navbar__links">
                <div
                  v-for="(link, index) in links"
                  :key="index"
                  class="navbar__item"
                  :class="[
                    ...(Array.isArray(link.className)
                      ? link.className
                      : link.className
                      ? [link.className]
                      : [])
                  ]"
                  @click="() => toggleMenu(false)"
                >
                  <router-link
                    :to="link.href"
                    class="navbar__link"
                    :style="link.style"
                  >
                    {{ link.label }}
                  </router-link>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </Teleport>
    </div>
  </nav>
</template>

<style lang="scss" scoped>
@use "@/assets/style" as *;

.navbar__backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  backdrop-filter: blur(6px);
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 999;
}

.navbar__logo {
  @include font-large;
  @include gradient-text;
  font-size: 2rem;
  padding: 1rem;
}
</style>

<style lang="scss" scoped>
.navbar {
  margin: 0 auto;
  position: sticky;
  top: 0;
  padding: 1rem;
  height: 6rem;
  background-color: rgb(var(--v-theme-background), 0.75);
  border: 2px solid rgb(var(--v-theme-primary));
  border-radius: var(--v-borderRadius);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--v-fontFamily);
  z-index: 1000;
}

.navbar__container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar__hamburger {
  display: none;
  font-size: 2rem;
  cursor: pointer;
  color: rgb(var(--v-theme-primary));
}

ul.navbar__links {
  display: flex;
  list-style: none;
  gap: 1rem;
  padding: 0.5rem;
  margin: 0;
}

ul .navbar__item {
  list-style: none;
}

ul .navbar__link {
  padding: 10px;
  text-decoration: none;
  color: rgb(var(--v-theme-text));
  font-weight: bold;
  transition: color 0.3s ease, background-color 0.3s ease;
}

ul .navbar__link--active {
  color: #fff;
  padding: calc(1rem + 4px);
  background-color: rgb(var(--v-theme-primary));
  border-radius: calc(var(--v-borderRadius) - 9px);
}

@media (max-width: 959px) {
  ul.navbar__links {
    display: none;
  }

  .navbar__hamburger {
    display: block;
  }
}

.navbar__sidebar.mobile {
  overflow-y: auto;
  position: fixed;
  top: 0;
  left: 0;
  width: 80%;
  max-width: 300px;
  height: 100vh;
  background-color: rgba(var(--v-theme-secondary), 110%);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 2rem 1rem;
  transform: translateX(-100%);
  transition: transform 0.3s ease-in-out;
  z-index: 1000;

  &.open {
    transform: translateX(0); 
  }

  .navbar__close {
    align-self: flex-end;
    font-size: 2rem;
    color: var(--v-theme-text);
    cursor: pointer;
    margin-bottom: 1rem;
  }

  .navbar__links {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .navbar__item {
    width: 100%;
    border-bottom: 1px solid rgba(255, 255, 255, 0.95);
    padding: 0.5rem 0;
  }

  .navbar__link {
    display: block;
    width: 100%;
    padding: 0.75rem 1rem;
    text-decoration: none;
    color: var(--v-theme-text);
    font-size: 1.2rem;
    font-weight: bold;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: rgb(var(--v-theme-primary));
      color: rgb(var(--v-theme-background));
    }
  }
}

.slide-menu-enter-active,
.slide-menu-leave-active {
  transition: transform 0.3s ease-in-out;
}

.slide-menu-enter, 
.slide-menu-leave-to  {
  transform: translateX(-100%);
}

.slide-menu-enter-to,
.slide-menu-leave-from {
  transform: translateX(0);
  opacity: 1;
}
</style>
