<template>
  <div class="app">
    <Navbar :links="navLinks">
      <template #logo>
        <img src="@/assets/vue.svg" alt="App Logo" />
      </template>
    </Navbar>

    <Hero :phrases="heroPhrases">
      <template #hero>
        <img src="@/assets/vue.svg" alt="Hero image" />
      </template>
    </Hero>
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
    
    <Footer :footerData="footerData">
      <template #logo>
        Plannder
        <!--img src="@/assets/vue.svg" alt="Hero image" /-->
      </template>
    </Footer>
  </div>
</template>

<script lang="ts" setup>
import Navbar from "@/components/Navbar.vue";
import Hero from "@/components/Hero.vue";
import Footer from "@/components/Footer.vue";
import FAQ from "@/components/section/FAQ.vue";
import Section from "@/components/Section.vue";
const navLinks = [
  { label: "Oferta", href: "/" },
  { label: "Kontakt", href: "/" },
  { label: "Panel", href: "/", active: true },
];

const heroPhrases = [
  { word: "Zaplanuj" },
  { word: ["przygodę", "podróż"], animation: true },
  { word: "która" },
  { word: "zapadnie" },
  { word: "w pamięć" },
  { word: "na zawsze" },
];

const footerData = {
  links: [
    { label: "Oferta", href: "/" },
    { label: "Kontakt", href: "/" },
    { label: "Panel", href: "/" },
  ],
  footerText: "© 2024 Plannder Wszystkie prawa zastrzeżone",
};
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

<style></style>
