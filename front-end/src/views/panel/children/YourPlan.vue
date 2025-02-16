<script setup lang="ts">
import Section from "@/components/Section.vue";
import TripBox from "@/components/TripBox.vue";
import { useTripStore } from "@/stores/tripStore";
const { yourTrips } = useTripStore();
//const { data: trips, isLoading, error, isSuccess } = yourTrips.trips()

import TripCard from "@/components/TripCard.vue";

const trips = [
  {
    title: "Wycieczka po Berlinie",
    location: "Berlin",
    dateRange: "12.12.2025 - 15.12.2025",
    actions: [
      {
        label: "Edytuj",
        color: "bg-primary",
        onClick: () => alert("Edytowanie wycieczki"),
      },
      {
        label: "Usuń",
        color: "bg-accent",
        onClick: () => alert("Usuwanie wycieczki"),
      },
    ],
  },
  {
    title: "Weekend w Paryżu",
    location: "Paryż",
    dateRange: "05.05.2025 - 07.05.2025",
    actions: [
    {
        label: "Edytuj",
        color: "bg-primary",
        onClick: () => alert("Edytowanie wycieczki"),
      },
      {
        label: "Usuń",
        color: "bg-accent",
        onClick: () => alert("Usuwanie wycieczki"),
      },
    ],
  },
];
</script>

<template>
  <v-container fluid class="full-width-container">
    <v-row>
      <v-col cols="12" md="10" offset-md="1">
        <Section>
          <template #content>
            <!--p v-if="isLoading">Ładowanie...</!--p>
            <p-- v-else-if="error">Błąd: {{ error.message }}</p-->
            <TripCard :trips="trips" />
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
