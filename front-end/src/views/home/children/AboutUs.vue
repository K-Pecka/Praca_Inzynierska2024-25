<script lang="ts" setup>
import TeamMemberCard from "@/components/TeamMemberCard.vue";

const aboutTeam = {
  mainTitle: "Dowiedź się więcej o nas",
  subTitle: "Nasz zespół",
  paragraphs: [
    `Nasz zespół składa się z czterech studentów informatyki, których połączyła pasja do tworzenia użytecznych i nowoczesnych rozwiązań technologicznych. 
    W ramach pracy inżynierskiej zdecydowaliśmy się stworzyć aplikację wspierającą zarządzanie podróżami grupowymi — z możliwością planowania trasy, budżetu, harmonogramu oraz uczestników.`,

    `Nasz pomysł zrodził się z osobistych doświadczeń: planowanie wspólnych wyjazdów z przyjaciółmi zawsze kończyło się chaosem. Nasza aplikacja ma to zmienić — 
    pozwala na przejrzyste zarządzanie wyjazdem, dzielenie się kosztami, a także lepszą komunikację między uczestnikami.`,

    `Podzieliliśmy się zadaniami według naszych mocnych stron: frontend, backend, DevOps i dokumentacja. Dzięki współpracy i zaangażowaniu stworzyliśmy funkcjonalne, responsywne i intuicyjne narzędzie, które może realnie ułatwić organizację podróży.`,
  ],
};

const teamMembers = [
  {
    name: "Andrzej Ebertowski",
    role: "...",
    description: "...",
  },
  {
    name: "Kacper Pecka",
    role: "Frontend Developer",
    description: "...",
  },
  {
    name: "Jakub Pobłocki",
    role: "Backend Developer",
    description: "...",
  },
  {
    name: "Mateusz Wiśnieiwski",
    role: "...",
    description: "...",
  },
];
</script>

<template>
  <v-container class="py-10">
    <h1 class="text-h4 text-center text-primary font-weight-bold mb-6">
      {{ aboutTeam.mainTitle }}
    </h1>

    <v-row justify="center" class="mb-10">
      <v-col cols="12" sm="10" offset-md="0" md="12">
        <div class="text-body-1 w-100">
          <p
            v-for="(paragraph, index) in aboutTeam.paragraphs"
            :key="index"
            class="text-justify"
            :class="{ 'mt-4': index > 0 }"
          >
            {{ paragraph }}
          </p>
        </div>
      </v-col>
    </v-row>
    <h2 class="text-h4 text-center text-primary font-weight-bold mb-6">
      {{ aboutTeam.subTitle }}
    </h2>
    
    <TeamMemberCard :members="teamMembers" />
  </v-container>
</template>
