<script lang="ts" setup>
import Navbar from '@/components/Navbar.vue';
const navLinks = [
  { label: "Oferta", href: "/" },
  { label: "Kontakt", href: "/"},
  { label: "Panel", href: "/",active:true}
];
</script>

<template>
  <Navbar :links="navLinks">
    <template #logo>
      <img src="@/assets/vue.svg" alt="App Logo" />
    </template>
  </Navbar>
</template>


