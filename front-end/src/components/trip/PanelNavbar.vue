<script setup lang="ts">
import {ref} from "vue";

const props = defineProps({
  accountIcon: String,
});

const accountMenuOpen = ref(false);

function toggleAccountMenu() {
  accountMenuOpen.value = !accountMenuOpen.value;
}
</script>

<template>
  <nav class="panel-navbar">
    <router-link class="panel-navbar__logo" to="/">
      <slot name="logo">
        <h1>Logo</h1>
      </slot>
    </router-link>

    <div class="panel-navbar__account" @click="toggleAccountMenu">
      <img
          :src="accountIcon"
          alt="Ikona konta"
          class="panel-navbar__icon"
      />
      <a href="#" class="panel-navbar__account-l">Moje Konto</a>

      <div
          v-if="accountMenuOpen"
          class="panel-navbar__dropdown"
      >
        <router-link
            to="/settings"
            class="dropdown-link"
        >
          Ustawienia konta
        </router-link>

        <router-link
            to="/panel"
            class="dropdown-link"
        >
          Wybór roli
        </router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped lang="scss">
@use "@/assets/style" as *;

.panel-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: rgba(#F5F4FC, 0.75);
  border-bottom: 2px solid rgb(var(--v-theme-primary));
  padding: 1rem 2rem;
  z-index: 1000;
}

.panel-navbar__logo {
  @include font-large;
  @include gradient-text;
  font-size: 2rem;
  padding: 0.5rem;
}

.panel-navbar__account {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  cursor: pointer;
}

.panel-navbar__icon {
  width: 36px;
  height: 36px;
}

.panel-navbar__account-l {
  text-decoration: none;
  color: rgb(var(--v-theme-text));
  font-weight: 500;
  transition: color 0.3s;

  &:hover {
    color: rgb(var(--v-theme-primary));
  }
}


.panel-navbar__dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
  padding: 0.5rem;
  margin-top: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  min-width: 165px;
  z-index: 1000;
}


.dropdown-link {
  display: block;
  padding: 0.5rem;
  text-decoration: none;
  color: #333;
  transition: background-color 0.2s, color 0.2s;

  &:hover {
    background-color: rgb(var(--v-theme-primary));
    color: white;
  }
}
</style>
