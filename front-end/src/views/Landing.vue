<template>
  <div class="app">
    <!-- Navbar Component -->
    <Navbar :links="navLinks">
      <template #logo>
        <img src="@/assets/vue.svg" alt="App Logo" />
      </template>
    </Navbar>

    <Hero :phrases="heroPhrases">
      <template #hero>
        <img src="@/assets/vue.svg" alt="Hero image" />
      </template>
    </Hero>
  </div>
</template>

<script lang="ts" setup>
import Navbar from "@/components/Navbar.vue";
import Hero from "@/components/Hero.vue";

const navLinks = [
  { label: "Oferta", href: "/" },
  { label: "Kontakt", href: "/" },
  { label: "Panel", href: "/", active: true },
];

const heroPhrases = [
  { word: "Zaplanuj" },
  { word: ["przygodę", "podróż"], animation: true},
  { word: "która" },
  { word: "zapadnie" },
  { word: "w pamięć" },
  { word: "na zawsze" },
];
</script>

<style></style>
