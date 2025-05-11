<script setup lang="ts">

import router from "@/router";
import {useTripStore, useAuthStore} from "@/stores";
import AppButton from "../AppButton.vue";

const {userData} = useAuthStore();
const {isOwner} = userData;
const {plan} = useTripStore()
const {handleDeleteItinerary} = plan;

function formatPL(dateString: string): string {
  const dateObj = new Date(dateString);
  if (isNaN(dateObj.getTime())) return dateString;
  return new Intl.DateTimeFormat('pl-PL').format(dateObj);
}

const props = defineProps<{
  isOwner: boolean,
  plans: any;
  btn: any;
}>();
</script>

<template>
  <v-row v-if="props.plans.length > 0" no-gutters>
    <v-col
        v-for="(trip, index) in plans"
        :key="index"
        cols="12"
        sm="12"
        md="12"
        lg="12"
        class="px-0"
    >
      <v-card
          class="trip-card background-secondary rounded-lg pa-8 flex-wrap"
          elevation="4"
      >
        <v-row no-gutters>
          <v-col
              cols="12"
              sm="8"
              md="8"
              lg="10"
              :class="{'text-center': $vuetify.display.smAndDown}"
          >
            <v-row align="center" no-gutters>
              <v-icon size="64" color="primary" class="mr-3">
                mdi-calendar-check
              </v-icon>
              <v-col>
                <v-card-title class="text-h5 font-weight-bold pa-0 color-text">
                  {{ trip.name }}
                </v-card-title>
                <v-card-subtitle class="px-0 pb-1 text-h6 font-weight-medium">
                  {{ trip.country }} {{ trip?.description ?? "brak opisu" }}
                </v-card-subtitle>
                <v-card-text class="pa-0 text-h6 font-weight-medium">
                  {{ formatPL(trip.start_date) }} - {{ formatPL(trip.end_date) }}
                  <span class="color-accent ml-2">{{ trip.activity_count }} aktywności</span>
                </v-card-text>
              </v-col>
            </v-row>
          </v-col>

          <!-- Buttons -->
          <v-col cols="12" sm="4" md="4" lg="2">
            <v-row
                no-gutters
                justify="center"
                justify-md="end"
                justify-lg="end"
                align="center"
                v-if="isOwner"
                class="h-100"
            >
              <AppButton
                  color="primary-outline"
                  @click="router.push({name: 'ActivityView', params: {planId: trip.id}})"
                  font-auto
                  :class="{'w-100' :$vuetify.display.smAndDown}"
                  max-width="190px"
                  text="Zarządzaj planem"
              />
              <AppButton
                  color="red"
                  @click="handleDeleteItinerary(trip.trip, trip.id)"
                  :class="{'w-100' :$vuetify.display.smAndDown}"
                  font-auto
                  max-width="190px"
                  text="Usuń plan"
              />
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>