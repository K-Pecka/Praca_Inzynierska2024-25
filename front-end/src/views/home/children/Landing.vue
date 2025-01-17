<template>
  <div>

      <Hero :phrases="heroPhrases">
      <template #hero>
        <img src="@/assets/hero.svg" alt="Hero image" />
      </template>
      </Hero>

      <Sections/>

  </div>
</template>

<script lang="ts" setup>
import Hero from "@/components/Hero.vue";
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

