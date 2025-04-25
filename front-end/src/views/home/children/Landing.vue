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
        transition="scale-transition"
      />
    </template>
  </Hero>

  <Sections />
</template>

<style scoped lang="scss">

.hero-image {
  min-width: 10rem;
  width: 16vw;
  transition: transform 0.3s ease-in-out;
}
</style>
