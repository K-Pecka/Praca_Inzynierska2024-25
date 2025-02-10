<script setup lang="ts">
import Section from "@/components/Section.vue";
import TripBox from "@/components/TripBox.vue";
import { useTripStore } from "@/stores/tripStore";
const { yourTrips } = useTripStore();
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="10" offset-md="1">
        <Section>
          <template #title>
            <h1>Zarządzaj wycieczami</h1>
          </template>
          <template #content>
            <TripBox :btn="yourTrips.btn" :trip="yourTrips.trip" />
          </template>
        </Section>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="10" offset-md="1">
        <Section>
          <template #title>
            <h1>Archiwum</h1>
          </template>
          <template #content>
            <TripBox :btn="yourTrips.btn" :trip="yourTrips.trip" />
          </template>
        </Section>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
h1 {
  font-size: 2.25rem;
  text-align: left;
}
</style>
