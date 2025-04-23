<script lang="ts" setup>
import {SubSection} from "@/components";
import { SubSectionData } from "@/types";


defineProps({
  subSections: {
    type: Array as () => SubSectionData[],
    required: true,
  },
});
</script>

<template>
  <section class="section-with-subsections">
    <SubSection
      v-for="(subSection, index) in subSections"
      :key="index"
      :items="subSection.items"
    >
      <template #title>
        {{ subSection.title }}
      </template>
    </SubSection>
  </section>
</template>

<style scoped lang="scss">
.section-with-subsections {
  margin: 2rem 0;

  &__title {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
  }
}
</style>
