<script lang="ts" setup>
import TypewriterText from "@/components/TypewriterText.vue";
import { Phrase } from "@/type";

const props = defineProps({
  phrases: {
    type: Array as () => Phrase[],
    required: true,
  },
});
</script>

<template>
  <header class="hero">
    <v-container fluid class="full-width-container">
      <v-row>
        <v-col cols="7" class="hero__text">
          <span v-for="(item, index) in phrases" :key="index" class="phrase">
            <TypewriterText
              v-if="item.animation"
              :phrases="[item]"
              class="hero__text__word"
              :style="item.styles"
            />
            <span v-else>
              {{ item.word }}
            </span>
          </span>
        </v-col>

        <v-col cols="5" class="hero__image">
          <slot name="hero"></slot>
        </v-col>
      </v-row>
    </v-container>
  </header>
</template>
<style scoped lang="scss">
@use "@/assets/style" as *;

.hero {
  padding: 1rem 0;

  @include font-large;

  &__text {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: -4px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
    transition: transform 0.3s ease;
    padding: 2rem 0;

    &__word {
      @include gradient-text;
    }

    @media (max-width: 600px) {
      margin-top: -2rem;
      font-size: 2rem;
    }
    @media (min-width: 600px) and (max-width: 800px) {
      font-size: 3rem;
    }
    @media (min-width: 800px) and (max-width: 1200px) {
      font-size: 3.5rem;
    }
  }

  &__image {
    display: flex;
    padding-top: 3%;
    justify-content: flex-end;
  }
}
</style>
