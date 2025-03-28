<script setup lang="ts">
import {Section,TripCard} from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";

const { yourPlans } = useTripStore();
import { useRoute } from "vue-router";

const route = useRoute();
const id = route.params.tripId as string;
const { data: rawPlans, isLoading, error } = yourPlans.plans(id);
</script>

<template>
  <v-container fluid class="full-width-container">
    <v-row>
      <v-col cols="12" md="10" offset-md="1">
        <Section>
          <template #content>
            <h1>Twoje plany</h1>
            <p v-if="isLoading">Ładowanie...</p>
            <p v-else-if="error">Błąd: {{ error.message }}</p>
            <template v-else> 
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
