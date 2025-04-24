<script lang="ts" setup>
import {Section,FAQ,Advantage} from "@/components";
import { usePageHomeStore } from "@/stores/ui/usePageHomeStore";
const useStore = usePageHomeStore();
const faqList = useStore.getFAQData(10);
const subSections = useStore.getAdvantagesData();
</script>

<template>
  <Section>
    <template #title>
      <h1
          class="gradient-text"
          style="
            font-size: clamp(
              1rem,
              4.5vw,
              20rem
            );
            line-height: 1;
            width: 80%;
            margin-bottom: 5vh;
          "
      >
        Co zyskasz korzystając z naszej aplikacji?
      </h1>
    </template>
    <template #content>
      <Advantage :subSections="subSections">
        <template #main-title></template>
      </Advantage>
    </template>
  </Section>
  <Section>
    <template #title>
      <span style="font-size: 3vw; font-weight: 700;">FAQ</span>
      <span style="font-size: 2vw;">Najczęściej zadawane pytania</span>
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
