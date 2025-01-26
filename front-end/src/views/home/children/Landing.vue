<template>
  <Hero :phrases="heroPhrases">
    <template #hero>
      <img src="@/assets/hero.svg" alt="Hero image" />
    </template>
  </Hero>

  <Sections />
</template>

<script lang="ts" setup>
import Hero from "@/components/home/Hero.vue";
import Sections from "@/components/section/Sections.vue";

const heroPhrases = [
  { word: "Zaplanuj" },
  { word: ["przygodę", "podróż"], animation: true },
  { word: "która" },
  { word: "zapadnie" },
  { word: "w pamięć" },
  { word: "na zawsze" },
];
</script>
<style scoped lang="scss">
img {
  transition: transform 0.3s ease;
  transform: scale(1.1) translate(10%, 0);

  @media (max-width: 600px) {
    transform: scale(0.5) translate(-40%, -40%);
  }
  @media (min-width: 600px) and (max-width: 800px) {
    transform: scale(0.75) translate(-10%, -10%);
  }
  @media (min-width: 800px) and (max-width: 1200px) {
    transform: scale(1) translate(0, 0);
  }
}
</style>
