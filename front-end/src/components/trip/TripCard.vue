<script setup lang="ts">

import router from "@/router";
import {usePlans} from "@/stores/trip/usePlans";
import {ref} from "vue";

const plansStore = usePlans();

function formatPL(dateString: string): string {
  const dateObj = new Date(dateString);
  if (isNaN(dateObj.getTime())) return dateString;
  return new Intl.DateTimeFormat('pl-PL').format(dateObj);
}

// onclick: (trip: string, id: string) =>
// router.push({ name: "ActivityView", params: { tripId: trip, planId: id } }),
const items = [
  {
    title: "Zarządzaj planem",
    class: "primary",
    icon: "mdi-pencil",
    onclick: (tripId: string, itineraryId: string) =>
        router.push({name: "ActivityView", params: {tripId: tripId, planId: itineraryId}}),
  },
  {
    title: "usuń plan",
    class: "red",
    icon: "mdi-trash-can-outline",
    onclick: (tripId: string, itineraryId: string) =>
        plansStore.handleDeleteItinerary(tripId, itineraryId),
  },
]

const props = defineProps<{
  plans: any;
  btn: any;
}>();

</script>

<template>
  <v-container fluid class="pa-3">
    <v-row v-if="props.plans.length > 0">
      <v-col
          v-for="(trip, index) in plans"
          :key="index"
          cols="12"
          sm="12"
          md="12"
          lg="12"
          class="px-0"
      >
        <v-card class="d-flex trip-card rounded-lg pa-5 flex-wrap" elevation="3">
          <v-row>
            <v-col cols="12" sm="8" md="9" lg="10">
              <v-card-title class="text-h6 font-weight-bold pa-0">
                {{ trip.name }}
              </v-card-title>
              <v-card-subtitle class="px-0 pb-1 font-weight-medium">
                {{ trip.country }} {{ trip?.description ?? "brak opisu" }}
              </v-card-subtitle>
              <v-card-text class="pa-0 font-weight-medium">
                {{ formatPL(trip.start_date) }} - {{ formatPL(trip.end_date) }}
                <span class="activity-number ml-2">{{ trip.activities_count || 0 }} aktywności</span>
              </v-card-text>
            </v-col>

            <!-- Buttons -->
            <v-col cols="12" sm="4" md="3" lg="2" class="d-flex flex-row justify-sm-end align-center">
              <v-btn
                  v-for="(action, i) in items"
                  :key="i"
                  @click="action.onclick(String(trip.trip),String(trip.id))"
                  variant="flat"
                  :style="{'min-width': 'auto', 'background-color': 'transparent'}"
                  class="px-2"
              >
                <v-icon size="32" contain :color="action.class">
                  {{ action.icon }}
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
.activity-number {
  color: rgb(var(--v-theme-accent), 0.75);
}

.trip-card {
  background-color: rgba(var(--v-theme-secondary), 0.5);
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}

</style>
