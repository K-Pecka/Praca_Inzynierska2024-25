<script lang="ts" setup>
import TeamMemberCard from "@/components/ui/TeamMemberCard.vue";
import { aboutTeam } from "@/data";


</script>

<template>
  <v-container class="py-10">
    <h1 class="text-h4 text-center text-primary font-weight-bold mb-6">
      {{ aboutTeam.mainTitle }}
    </h1>

    <v-row justify="center" class="mb-10">
      <v-col cols="12" sm="12" offset-md="0" md="10">
        <div class="text-body-1 w-100">
          <div
            v-for="(paragraph, index) in aboutTeam.paragraphs"
            :key="index"
          >
            <h2 class="text-h5 my-4 text-primary font-weight-bold">{{ paragraph.title }}</h2>
            <p class="text-justify">{{ paragraph.paragraph }}</p>
            <template v-if="index == 0 ">
              <v-divider class="my-4" color="grey lighten-2" height="2px" width="100%" />
              <TeamMemberCard :members="aboutTeam.teamMembers" />
            </template>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
