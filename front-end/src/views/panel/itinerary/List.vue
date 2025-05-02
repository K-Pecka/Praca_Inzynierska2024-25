<script setup lang="ts">
import { Section, TripCard } from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import HeaderSection from "@/components/common/HeaderSection.vue";

const { yourPlans, getTripDetails } = useTripStore();
import { useRoute } from "vue-router";

const route = useRoute();
const id = route.params.tripId as string;
const { data: rawPlans, isLoading, error } = yourPlans.plans(id);
const { data: trip_data } = getTripDetails(Number(id));
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection>
        <template #subtitle>
          <h2 class="trip-title">
            Plany podróży
          </h2>
        </template>
      </HeaderSection>
    </template>
    <template #content>
      <p v-if="isLoading">Ładowanie...</p>
      <p v-else-if="error">Błąd: {{ error.message }}</p>
      <template v-else-if="trip_data">
        <TripCard :plans="rawPlans" :btn="yourPlans.btn ?? []" />
      </template>
    </template>
  </Section>
</template>

