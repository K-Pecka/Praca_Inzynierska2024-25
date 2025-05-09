<script lang="ts" setup>
import TeamMemberCard from "@/components/ui/TeamMemberCard.vue";
import Section from "@/components/common/Section.vue";
import { aboutTeam } from "@/data";
</script>

<template>
  <Section class="pb-10">
    <template #title>
      <h1 class="text-h4 text-center text-primary font-weight-bold mb-6">
          {{ aboutTeam.mainTitle }}
        </h1>
    </template>
    <template #content>
      <v-container>
        <v-row justify="center" class="mb-10">
          <v-col cols="12" sm="12" offset-md="0" md="10">
            <div class="text-body-1 w-100">
              <div
                v-for="(paragraph, index) in aboutTeam.paragraphs"
                :key="index"
              >
                <span class="text-h5 my-4 text-black-70 font-weight-bold">
                  {{ paragraph.title }}
                </span>
                <p class="text-justify">{{ paragraph.paragraph }}</p>
                <template v-if="index == 0">
                  <TeamMemberCard :members="aboutTeam.teamMembers" />
                </template>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </Section>
</template>