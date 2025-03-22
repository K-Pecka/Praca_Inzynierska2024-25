<script lang="ts" setup>
import { Hero, Sections } from "@/components";
import { usePageHomeStore } from "@/stores";
import { image } from "@/lib";

const { getHeroBannerText } = usePageHomeStore();
</script>

<template>
  <Hero :phrases="getHeroBannerText()">
    <template #hero>
      <img
        :src="image.hero.img"
        :alt="image.hero.alt"
        class="hero-image"
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
  position: relative;
  top: -5%;
  @media (max-width: 600px) {
    transform: scale(0.5) translateX(100%);
    top: -3%;
    display:none;
  }
  @media (min-width: 600px) and (max-width: 800px) {
    transform: scale(0.75) translateX(30%);
    top: -1%;
    display:none;
  }
  @media (min-width: 800px) {
    transform: scale(1);
    top: 0%;
  }
}
</style>
