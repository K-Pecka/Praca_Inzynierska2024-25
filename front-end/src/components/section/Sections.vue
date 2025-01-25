<script lang="ts" setup>
import Section from "@/components/Section.vue";
import FAQ from "@/components/section/FAQ/FAQ.vue";
import Advantage from "@/components/section/Advantage/Advantage.vue";
const faqList = [
  {
    question: "Czy mogę zaplanować podróż grupową?",
    answer: "Tak! Aplikacja umożliwia planowanie podróży grupowych. Możesz zaprosić inne osoby, aby razem edytować plan, głosować nad miejscami do odwiedzenia lub śledzić wspólne wydatki.",
  },
  {
    question: "Czy aplikacja jest płatna?",
    answer: "Aplikacja oferuje darmowy plan z podstawowymi funkcjami. Możesz także wykupić subskrypcję premium, która odblokowuje dodatkowe opcje, takie jak zaawansowane mapy, wskazówki offline i personalizowane rekomendacje.",
  },
  {
    question: "Czy aplikacja śledzi mój budżet podróży?",
    answer: "Tak, w aplikacji znajduje się funkcja budżetowania, która pozwala dodawać wydatki i monitorować koszty w czasie rzeczywistym. Możesz także ustawić limit budżetu na całą podróż.",
  },
];
const subSections = [
  {
    title: "Jako Turysta",
    items: [
      {
        image: "picture/p1.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "picture/p2.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "picture/p3.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "picture/p4.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
    ],
  },
  {
    title: "Jako Przewodnik",
    items: [
      {
        image: "picture/p1.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "picture/p2.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "picture/p3.svg",
        alt: "picture",
        caption: "Elastyczny planer podróży",
      },
      {
        image: "picture/p4.svg",
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
