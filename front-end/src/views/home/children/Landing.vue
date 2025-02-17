<script lang="ts" setup>
import {Hero,Sections} from "@/components";
import { usePageStore } from "@/stores";
import {image} from "@/lib"
const { heroText } = usePageStore();
</script>

<template>
  <Hero :phrases="heroText()">
    <template #hero>
      <img :src="image.hero.img" :alt=image.hero.alt />
    </template>
  </Hero>

  <Sections />
</template>

<style scoped lang="scss">//TODO: style poprawić
img {
  transform-origin: top left;
  transition: transform 0.3s ease;
  transform: scale(0.8) translateX(-10%);

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
