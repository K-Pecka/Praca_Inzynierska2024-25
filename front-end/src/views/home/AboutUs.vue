<script lang="ts" setup>
import TeamMemberCard from "@/components/ui/TeamMemberCard.vue";
import Section from "@/components/shared/Section.vue";
import { aboutTeam } from "@/data";
import { HeaderSection } from "@/components";
</script>

<template>
  <Section class="pb-10">
    <template #title>
      <HeaderSection
        title="Nasz"
        title-gradient-text="Zespół"
        no-sub-title
        center
      />
    </template>
    <template #content>
      <v-row justify="center" class="mb-10">
        <v-col cols="12" sm="12" offset-md="0" md="10">
          <div>
            <span class="text-h5 text-justify">
              Jesteśmy grupą studentów, których połączyła pasja do podróży i
              chęć ułatwienia życia sobie i innym. Z własnego doświadczenia
              wiemy, jak trudno czasem zorganizować wspólny wyjazd — dlatego
              stworzyliśmy aplikację, która to upraszcza . Nie chcemy nikomu nic
              narzucać – dajemy jedynie narzędzia, które pozwalą zaplanować
              podróż dokładnie tak, jak chcecie . Prosto, wygodnie i po swojemu.
            </span>
          </div>
          <div class="text-body-1">
            <div
              v-for="(paragraph, index) in aboutTeam.paragraphs"
              :key="index"
            >
              <template v-if="index == 0">
                <TeamMemberCard :members="aboutTeam.teamMembers" />
              </template>
            </div>
          </div>
        </v-col>
      </v-row>
    </template>
  </Section>
</template>
