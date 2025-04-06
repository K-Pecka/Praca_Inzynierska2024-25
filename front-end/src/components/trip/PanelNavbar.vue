<script setup lang="ts">
import {ref} from "vue";

const props = defineProps({
  accountIcon: String,
  showNavigation: Boolean,
});

const accountMenuOpen = ref(false);

function toggleAccountMenu() {
  accountMenuOpen.value = !accountMenuOpen.value;
}

const emit = defineEmits(["toggleMenu"]);

function onHamburgerClick() {
  emit("toggleMenu");
}
</script>

<template>
  <nav class="panel-navbar">
    <router-link class="panel-navbar__logo" to="/">
      <slot name="logo">
        <h1>Logo</h1>
      </slot>
    </router-link>

    <div v-if="showNavigation" class="panel-navbar__hamburger" @click="onHamburgerClick">
      <v-icon size="46">mdi-menu</v-icon>
    </div>

    <div class="panel-navbar__account" @click="toggleAccountMenu">
      <!--      <v-icon
                class="panel__account-icon"
                size="34"
            >{{accountIcon}}</v-icon>-->
      <v-avatar class="panel__account-avatar" color="primary" size="36" variant="elevated">
        <span class="text-h6">
    {{ accountIcon }}
        </span>
      </v-avatar>

      <router-link :to="{}" class="panel-navbar__account-l">Moje Konto</router-link>

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
  background-color: rgba(var(--v-theme-background));
  border-bottom: 2px solid rgb(var(--v-theme-primary));
  padding: 1rem 2rem;
  z-index: 1000;
  height: 5rem;
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

.panel-navbar__account-l {
  text-decoration: none;
  color: rgb(var(--v-theme-text));
  font-weight: 500;
  transition: color 0.3s;

  &:hover {
    color: rgb(var(--v-theme-primary));
  }
}

.panel__account-icon {
  color: rgb(var(--v-theme-accent));
}

.panel-navbar__dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;/* ! */;	
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

.panel-navbar__hamburger {
  display: none;
  font-size: 2rem;
  cursor: pointer;
  color: rgb(var(--v-theme-primary));
}

@media (max-width: 1000px) {
  .panel-navbar__hamburger {
    display: block;
  }
}

</style>
