<script lang="ts" setup>
import { ref } from "vue";
import { Link } from "@/type";


defineProps<{ links: Link[] }>();

const menuOpen = ref(false);

const toggleMenu = () => {
  document.documentElement.style.overflow = menuOpen.value ? "auto" : "hidden";
  menuOpen.value = !menuOpen.value;
};
</script>

<template>
  <nav class="navbar">
    <div class="navbar__container">
      
      <router-link to="/" class="navbar__logo">
        <slot name="logo">
          <h1>Logo</h1>
        </slot>
      </router-link>

      <div class="navbar__hamburger" @click="toggleMenu">&#9776;</div>

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
              : []),
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
        <div class="navbar__overlay mobile" v-if="menuOpen">
          <div class="navbar__close" @click="toggleMenu">X</div>
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
                  : []),
              ]"
            >
              <router-link :to="link.href" class="navbar__link" :style="link.style">
                {{ link.label }}
              </router-link>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </nav>
</template>
<style lang="scss" scoped>
@use "@/assets/style" as *;
a {
  text-decoration: none;
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
  background-color: rgb(var(--v-theme-background),0.75);
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

.navbar__logo {
  font-size: 2rem;
  padding: 1rem;
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

@media (max-width: 768px) {
  ul.navbar__links {
    display: none;
  }
  .navbar__hamburger {
    display: block;
  }
}

.navbar__overlay.mobile {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.95);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.mobile .navbar__close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 2rem;
  color: white;
  cursor: pointer;
}

.mobile .navbar__links {
  display: flex;
  flex-direction: column;
  width: 90%;
  max-width: 400px;
  gap: 1rem;
  text-align: center;
}

.mobile .navbar__item {
  width: 100%;
  background-color: transparent;
  transition: background-color 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.6);
  border-top: 1px solid rgba(255, 255, 255, 0.6);
}

.mobile .navbar__item:hover {
  background-color: rgb(var(--v-theme-primary));
  color: white;
}

.mobile .navbar__link {
  display: block;
  padding: 15px;
  text-decoration: none;
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  transition: color 0.3s ease;
}
</style>
