<script setup lang="ts">
import Section from "@/components/Section.vue";
import TripBox from "@/components/TripBox.vue";
import { useTripStore } from "@/stores/tripStore";
const { yourTrips } = useTripStore();
const { data: trips, isLoading, error, isSuccess } = yourTrips.trips()
</script>

<template>
  <v-container fluid class="full-width-container">
    <v-row>
      <v-col cols="12" md="10" offset-md="1">
        <Section>
          <template #title>
            <h1>Zarządzaj utworzonymi planami</h1>
            <RouterLink to="/"></RouterLink>
          </template>
          <template #content>
            <p v-if="isLoading">Ładowanie...</p>
            <p v-else-if="error">Błąd: {{ error.message }}</p>
            <TripBox :btn="yourTrips.btn" :trip="trips ?? []" image="/picture/p1.svg" />
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
