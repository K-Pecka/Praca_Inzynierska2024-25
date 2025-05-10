<script setup lang="ts">

import router from "@/router";
import { useTripStore,useAuthStore } from "@/stores";
import { computed } from "vue";
const { userData } = useAuthStore();
const { isOwner } = userData;
const {plan} = useTripStore()
const {handleDeleteItinerary}=plan;
function formatPL(dateString: string): string {
  const dateObj = new Date(dateString);
  if (isNaN(dateObj.getTime())) return dateString;
  return new Intl.DateTimeFormat('pl-PL').format(dateObj);
}

const props = defineProps<{
  isOwner:boolean,
  plans: any;
  btn: any;
}>();
const btnValue = computed(()=> props.btn.filter((btn:{showIfOwner:boolean})=> btn.showIfOwner == props.isOwner))
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
        <v-card class="trip-card background-secondary rounded-lg pa-5 flex-wrap" elevation="4">
          <v-row>
            <v-col cols="12" sm="8" md="9" lg="10">
              <v-card-title class="text-h5 font-weight-bold pa-0">
                {{ trip.name }}
              </v-card-title>
              <v-card-subtitle class="px-0 pb-1 font-weight-medium">
                {{ trip.country }} {{ trip?.description ?? "brak opisu" }}
              </v-card-subtitle>
              <v-card-text class="pa-0 font-weight-medium">
                {{ formatPL(trip.start_date) }} - {{ formatPL(trip.end_date) }}
                <span class="color-accent ml-2">{{ trip.activity_count}} aktywności</span>
              </v-card-text>
            </v-col>

            <!-- Buttons -->
            <v-col cols="12" sm="4" md="3" lg="2" class="d-flex flex-row justify-sm-end align-center">
              <v-btn
                  v-for="(action, i) in btnValue"
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