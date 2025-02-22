<script lang="ts" setup>
import Section from "@/components/Section.vue";
import FAQ from "@/components/home/section/FAQ/FAQ.vue";
import Advantage from "@/components/home/section/Advantage/Advantage.vue";
import { usePageHomeStore } from "@/stores/ui/usePageHomeStore";
const useStore = usePageHomeStore();
const faqList = useStore.getFAQData(10);
const subSections = useStore.getAdvantagesData();
</script>

<template>
  <Section>
    <template #title>
      <h1 class="gradient-text">Co zyskasz korzystając z naszej aplikacji?</h1>
    </template>
    <template #content>
      <Advantage :subSections="subSections">
        <template #main-title></template>
      </Advantage>
    </template>
  </Section>
  <Section>
    <template #title>
      <h2>FAQ</h2>
      <span>Najczęściej zadawane pytania</span>
    </template>
    <template #content>
      <FAQ :faqList="faqList">
        <template #question="{ question }">
          <strong>{{ question }}</strong>
        </template>
        <template #answer="{ answer }">
          <p>{{ answer }}</p>
        </template>
      </FAQ>
    </template>
  </Section>
</template>
