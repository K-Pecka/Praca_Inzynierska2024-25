<script lang="ts" setup>
import Section from "@/components/Section.vue";
import FAQ from "@/components/section/FAQ/FAQ.vue";
import Advantage from "@/components/section/Advantage/Advantage.vue";
const faqList = [
  {
    question: "?",
    answer: "...",
  },
  {
    question: "?",
    answer: "...",
  },
  {
    question: "?",
    answer: "...",
  },
];
const subSections = [
  {
    title: "Jako Turysta",
    items: [
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
    ],
  },
  {
    title: "Jako Przewodnik",
    items: [
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "@/assets/vue.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
    ],
  },
];
</script>

<template>
  <Section>
    <template #title
      ><h1 class="gradient-text">
        Co zyskasz korzystając z naszej aplikacji?
      </h1></template
    >
    <template #content>
      <Advantage :subSections="subSections">
        <template #main-title>Gallery of Art</template>
      </Advantage>
    </template>
  </Section>
  <Section>
    <template #title
      ><h2>FAQ</h2>
      <span>Najczęściej zadawane pytania</span></template
    >
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
