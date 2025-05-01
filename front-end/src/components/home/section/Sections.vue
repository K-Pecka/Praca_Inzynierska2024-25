<script lang="ts" setup>
  import { Section, FAQ, Advantage } from "@/components";
  import { usePageHomeStore } from "@/stores/ui/usePageHomeStore";

  import { useDisplay } from 'vuetify'

  const { smAndDown } = useDisplay()

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
  <div class="d-flex flex-column align-center" :class="{ 'text-center': smAndDown }" style="width: 73%;">
    <span style="font-size: 50px; font-weight: 700;">FAQ</span>
    <span style="font-size: 28px;">Najczęściej zadawane pytania</span>
  </div>

  <FAQ :faqList="faqList" class="mb-16">
    <template #question="{ question }">
      <strong>{{ question }}</strong>
    </template>
    <template #answer="{ answer }">
      <p>{{ answer }}</p>
    </template>
  </FAQ>
</template>
