<template>
    <section class="section-with-subsections">
      <SubSection v-for="(subSection, index) in subSections" :key="index" :items="subSection.items">
        <template #title>
          {{ subSection.title }}
        </template>
      </SubSection>
    </section>
  </template>
  
  <script lang="ts" setup>
  import SubSection from '@/components/section/Advantage/SubSection.vue';
  
  interface SubSectionData {
    title: string;
    items: {
      image: string;
      alt: string;
      caption: string;
    }[];
  }
  
  defineProps({
    subSections: {
      type: Array as () => SubSectionData[],
      required: true,
    },
  });
  </script>
  
  <style scoped lang="scss">
  .section-with-subsections {
    margin: 2rem;
  
    &__title {
      font-size: 2.5rem;
      margin-bottom: 2rem;
      text-align: center;
    }
  }
  </style>
  