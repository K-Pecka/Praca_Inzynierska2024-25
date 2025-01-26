<script lang="ts" setup>
import Hero from "@/components/home/Hero.vue";
import Sections from "@/components/home/section/Sections.vue";
import { usePageStore } from "@/stores/pageContentStore";
const useStore = usePageStore();

const heroPhrases = useStore.heroTestData();
</script>

<template>
  <Hero :phrases="heroPhrases">
    <template #hero>
      <img src="@/assets/hero.svg" alt="Hero image" />
    </template>
  </Hero>

  <Sections />
</template>

<style scoped lang="scss">
img {
  transform-origin: top left;
  transition: transform 0.3s ease;
  transform: scale(1.1) translateX(-10%);

  @media (max-width: 600px) {
    transform: scale(0.5) translateX(100%);
  }
  @media (min-width: 600px) and (max-width: 800px) {
    transform: scale(0.75) translateX(30%);
  }
  @media (min-width: 800px) and (max-width: 1200px) {
    transform: scale(1);
  }
}
</style>
