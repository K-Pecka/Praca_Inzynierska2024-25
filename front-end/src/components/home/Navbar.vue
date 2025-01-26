<script lang="ts" setup>
import { ref } from 'vue';

interface Link {
  label: string;
  href: string;
  className?: string | string[];
  style?: Record<string, string>;
  active?: boolean;
}

defineProps<{ links: Link[] }>();

const menuOpen = ref(false);

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};
</script>

<template>
  <nav class="navbar">
    <div class="navbar__container">
      <div class="navbar__logo">
        <slot name="logo">
          <h1>Logo</h1>
        </slot>
      </div>
    
      <div
        class="navbar__hamburger"
        @click="toggleMenu"
      >
        &#9776;
      </div>
      <ul
        class="navbar__links"
        :class="{ open: menuOpen }"
      >
        <li v-for="(link, index) in links" :key="index" class="navbar__item"
        :class="[...(Array.isArray(link.className) ? link.className : link.className ? [link.className] : [])]">
          <a
            :href="link.href"
            class="navbar__link"
            :class="{
              'navbar__link--active': link.active
            }"
            :style="link.style"
            aria-current="page"
          >
            {{ link.label }}
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<style lang="scss" scoped>
@use "@/assets/style" as *;

.navbar {
  margin: .5rem auto;
  position: sticky;
  padding: 1rem;
  height: 6rem;
  background-color: var(--background-color);
  border: 2px solid var(--primary-color);
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--font-family);
  transition: all 0.3s ease-in-out;

  .navbar__container {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .navbar__logo {
    @include font-large;
    @include gradient-text;
    font-size: 2rem;
    padding: 1rem;
  }

  .navbar__links {
    display: flex;
    list-style: none;
    gap: 1rem;
    padding: 0.5rem;
    margin: 0;
  }

  .navbar__item {
    list-style: none;
  }

  .navbar__link {
    padding: 10px;
    text-decoration: none;
    color: var(--text-color);
    font-weight: bold;
    transition: color 0.3s ease, background-color 0.3s ease;

    &.navbar__link--active {
      color: #fff;
      padding: calc(1rem + 4px);
      background-color: var(--primary-color);
      border-radius: calc(var(--border-radius) - 9px);
    }
  }

  .navbar__hamburger {
    display: none;
    cursor: pointer;
  }

  @media (max-width: 768px) {
    .navbar__links {
      display: none;
      flex-direction: column;
      position: absolute;
      top: 6rem;
      right: 0;
      width: 100%;
      background-color: var(--background-color);
      border-top: 2px solid var(--primary-color);
    }

    .navbar {
      margin-top: 1vh;
    }

    .navbar__hamburger {
      display: block;
      font-size: 2rem;
      color: var(--primary-color);
    }
  }
}
</style>
