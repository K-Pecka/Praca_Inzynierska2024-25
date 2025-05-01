<script lang="ts" setup>
import TypewriterText from "@/components/common/TypeWriterText.vue";
import { Phrase } from "@/types";

const props = defineProps({
  phrases: {
    type: Array as () => Phrase[],
    required: true,
  },
});
</script>

<template>
  <header class="hero">
    <v-container fluid>
      <v-row>
        <v-col :cols="$vuetify.display.smAndDown ? 12 : 7"
        class="hero__text" ref="heroText"
        :class="{ 'justify-center align-center text-center': $vuetify.display.smAndDown }"
        >
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

        <v-col v-if="!$vuetify.display.smAndDown" cols="5" class="hero__image" ref="heroImage" >
          <slot name="hero"></slot>
        </v-col>
      </v-row>
    </v-container>
  </header>
</template>
<style scoped lang="scss">
@use "@/assets/styles/style" as *;
.hero__image{
  fill: rgb(var(--v-theme-hero-bg));
}
.hero {
  padding-top: 5%;
  margin-bottom: 20%;
  width: 70%;
  @include font-large;
  &__text {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -4px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
    transition: transform 0.3s ease;
    padding: 2rem 0;

    &__word {
      @include gradient-text;
    }
    font-size: clamp(2rem, 4.5vw, 30rem);
    line-height: 1;

    @media (max-width: 959px) {
      font-size: 10vw;
    }
  }

  &__image {
    display: flex;
    justify-content: flex-end;
  }
}
</style>
