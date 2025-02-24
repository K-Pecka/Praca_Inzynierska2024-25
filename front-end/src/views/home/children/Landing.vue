<script lang="ts" setup>
import { Hero, Sections } from "@/components";
import { usePageHomeStore } from "@/stores";
import { image } from "@/lib";

const { getHeroBannerText } = usePageHomeStore();
</script>

<template>
  <Hero :phrases="getHeroBannerText()">
    <template #hero>
      <v-img
        :src="image.hero.img"
        :alt="image.hero.alt"
        class="hero-image"
        contain
        lazy-src="/images/placeholder.jpg"
        transition="scale-transition"
      />
    </template>
  </Hero>

  <Sections />
</template>

<style scoped lang="scss">
// TODO: Poprawiona responsywność + płynniejsze animacje
.hero-image {
  max-width: 100%;
  transition: transform 0.3s ease-in-out;
  transform-origin: top left;

  @media (max-width: 600px) {
    transform: scale(0.5) translateX(100%);
  }
  @media (min-width: 600px) and (max-width: 800px) {
    transform: scale(0.75) translateX(30%);
  }
  @media (min-width: 800px) {
    transform: scale(1);
  }
}
</style>
