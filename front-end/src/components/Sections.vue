<script lang="ts" setup>
import FAQ from "@/components/section/FAQ.vue";
import Section from "@/components/Section.vue";
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
</script>

<template>
    <Section>
        <template #title><h1 class="gradient-text">Co zyskasz korzystając z naszej aplikacji?</h1></template>
    </Section>
    <Section>
      <template #title><h2>FAQ</h2><span>Najczęściej zadawane pytania</span></template>
      <template #content>
        <FAQ
        :faqList=faqList
        >
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