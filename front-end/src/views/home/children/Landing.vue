<script lang="ts" setup>
import { Hero, Sections } from "@/components";
import { usePageHomeStore } from "@/stores";
import { images } from "@/data";

const { getHeroBannerText } = usePageHomeStore();
</script>

<template>
  <Hero :phrases="getHeroBannerText()">
    <template #hero>
      <img
        :src="images.hero.img"
        :alt="images.hero.alt"
        class="hero-image"
        lazy-src="/images/placeholder.jpg"
        transition="scale-transition"
      />
    </template>
  </Hero>

  <Sections />
</template>

<style scoped lang="scss">

.hero-image {
  max-width: 100%;
  transition: transform 0.3s ease-in-out;
  @media (min-width: 800px) {
    transform: scale(0.9);
  }
}
</style>
