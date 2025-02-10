<script setup lang="ts">
import { defineProps, ref } from "vue";

defineProps({
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


    <div class="panel-navbar__account">
      <v-icon>fa-solid fa-house</v-icon>
      <img :src="accountIcon" alt="Ikona konta" class="panel-navbar__icon" />
      <a href="#" class="panel-navbar__account-l">Moje Konto</a>
    </div>
  </nav>
</template>

<style scoped lang="scss">
@use "@/assets/style" as *;
.panel-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: rgba(#F5F4FC,0.75);
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
</style>