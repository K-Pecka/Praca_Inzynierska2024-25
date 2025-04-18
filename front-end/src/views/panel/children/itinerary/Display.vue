<script setup lang="ts">
import {Section,TripCard} from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";

const { yourPlans, getTripDetails } = useTripStore();
import { useRoute } from "vue-router";

const route = useRoute();
const id = route.params.tripId as string;
const { data: rawPlans, isLoading, error } = yourPlans.plans(id);
const { data:trip_data } = getTripDetails(Number(id));
</script>

<template>
  <v-container fluid class="full-width-container">
    <v-row class="d-flex align-center">
      <v-col cols="12" md="12" offset-md="1" class="mx-0" >
        <Section>
          <template #content>
            <p v-if="isLoading">Ładowanie...</p>
            <p v-else-if="error">Błąd: {{ error.message }}</p>
            <template v-else-if="trip_data">
              <h1>{{ trip_data.name }}</h1>
              <TripCard
                :plans="rawPlans"
                :btn="yourPlans.btn ?? []"
              />
            </template>
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
