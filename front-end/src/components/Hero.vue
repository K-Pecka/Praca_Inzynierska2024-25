<template>
  <header class="hero">
    <div class="hero__text">
      <span v-for="(item, index) in phrases" :key="index" class="phrase">
        <TypewriterText v-if="item.animation" :phrases="[item]" class="word" :style="item.styles"/>
        <span v-else>
          {{ item.word }}
        </span>
      </span>
    </div>

    <div class="hero__image">
      <slot name="hero">
          <h1>Logo</h1>
        </slot>
    </div>
    <!--div class="circle"></div-->
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
@use '@/assets/style' as *;
header{
  position: relative;
}
.circle
{
  border-radius: 50%;
  background-color: var(--secondary-color);
  width:  55vw;
  height: 55vw;
  position: absolute;
  z-index: -1;
  left: 40vw;
  bottom:2vh;
}
.hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 66.6vw;
  margin: auto;
  padding: 1rem;
}
.word
{
  @include gradient-text;
}
.hero__text {
  flex: 3;
  flex-direction: column;
  text-transform: uppercase;
  @include font-large;
  font-weight: 600;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
  letter-spacing: -4%;
  padding: 2rem;
  display: flex;
  align-items: flex-start;
  height: 100%;
}

.hero__image {
  flex: 1;
  img {
    max-width: 100%;
    height: auto;
    border-radius: 10px;
  }
}
</style>
