<script setup lang="ts">
import Section from "@/components/Section.vue";
import TripBox from "@/components/TripBox.vue";
import { useTripStore } from "@/stores/tripStore";
import TripCard from "@/components/TripCard.vue";

const { yourPlans } = useTripStore();
import { useRoute } from "vue-router";

const route = useRoute();
const id = route.params.tripId as string;
const { data: rawPlans, isLoading, error, isSuccess } = yourPlans.plans(id);
</script>

<template>
  <v-container fluid class="full-width-container">
    <v-row>
      <v-col cols="12" md="10" offset-md="1">
        <Section>
          <template #content>
            <p v-if="isLoading">Ładowanie...</p>
            <p v-else-if="error">Błąd: {{ error.message }}</p>
            <template v-else>
            
              <h1>Twoje plany</h1>
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
