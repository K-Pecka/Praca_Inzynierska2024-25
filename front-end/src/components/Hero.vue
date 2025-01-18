<template>
  <header class="hero">
    <v-container fluid class="full-width-container">
      <v-row>
        <v-col cols="7" class="hero__text">
          <span v-for="(item, index) in phrases" :key="index" class="phrase">
            <TypewriterText
              v-if="item.animation"
              :phrases="[item]"
              class="word"
              :style="item.styles"
            />
            <span v-else>
              {{ item.word }}
            </span>
          </span>
        </v-col>

        <v-col cols="5" class="hero__image">
          <div class="wrapper">
            <slot name="hero">
              <img :src="imageSrc" alt="Hero image" />
            </slot>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </header>
</template>

<script lang="ts" setup>
import TypewriterText from "./TypewriterText.vue";
import { PropType } from "vue";
const imageSrc = "@/assets/your-image.jpg";
interface Phrase {
  word: string | string[];
  animation?: boolean;
  styles?: Record<string, string>;
}
const props = defineProps({
  phrases: {
    type: Array as PropType<Phrase[]>,
    required: true,
  },
});
</script>

<style scoped lang="scss">
@use "@/assets/style" as *;
header {
  position: relative;
}
.circle {
  border-radius: 50%;
  background-color: var(--secondary-color);
  width: 55vw;
  height: 55vw;
  position: absolute;
  z-index: -1;
  left: 40vw;
  bottom: 2vh;
}
.hero {
  margin: 1rem;
  padding: 1rem 0;
}
.word {
  @include gradient-text;
}
.hero__text {
  flex-direction: column;
  text-transform: uppercase;
  @include font-large;
  font-weight: 600;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
  letter-spacing: -4px;
  padding: 2rem 0;
  display: flex;
  align-items: flex-start;
}
.wrapper {
  position: relative;
}
.hero__text {
  font-size: 4rem;
  transition: transform 0.3s ease;
  @media (max-width: 600px) {
    font-size:2rem;
  }
  @media (min-width: 600px) and (max-width: 800px) {
    font-size:3rem;
  }
  @media (min-width: 800px) and (max-width: 1200px) {
    font-size: 3.5rem;
  }
}
</style>
