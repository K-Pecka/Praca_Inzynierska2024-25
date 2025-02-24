<script lang="ts" setup>
import { ref, onMounted } from "vue";
import Typewriter from "typewriter-effect/dist/core";
import { Phrase } from "@/type";

const props = defineProps({
  phrases: {
    type: Array as () => Phrase[],
    required: true,
  },
});

const typewriterRef = ref<HTMLDivElement | null>(null);

const animateText = () => {
  const typewriter = new Typewriter(typewriterRef.value as HTMLElement, {
    loop: true,
    delay: 75,
  });

  props.phrases.forEach((item) => {
    if (Array.isArray(item.word)) {
      item.word.forEach((word) => {
        typewriter.typeString(word).pauseFor(1000).deleteAll();
      });
    } else {
      typewriter
        .typeString(item.word as string)
        .pauseFor(1000)
        .deleteAll()
        .start();
    }
  });
  typewriter.start();
};

onMounted(() => {
  animateText();
});
</script>

<template>
  <div ref="typewriterRef">
    <div>
      <span v-for="(item, index) in phrases" :key="index">
        <span class="animated">
          <span
            v-for="(word, wordIndex) in Array.isArray(item.word)
              ? item.word
              : [item.word]"
            :key="wordIndex"
          >
            {{ word }}
          </span>
        </span>
      </span>
    </div>
  </div>
</template>

<style>
.Typewriter__cursor {
  color: rgb(var(--v-theme-accent));
}
</style>
