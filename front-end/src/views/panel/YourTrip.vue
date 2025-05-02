<script setup lang="ts">
import {useTripStore} from "@/stores/trip/useTripStore";
import {useRoute} from "vue-router";
import {useUtilsStore} from "@/stores";
import { images } from "@/data";

useTripStore().initialize(useRoute().name as string);

const {yourTrips} = useTripStore();
const {data: trips} = yourTrips.trips()
const {formatDatePolish} = useUtilsStore();

</script>

<template>
  <v-col cols="12">
    <v-row class="trip-wrapper mx-auto w-100" dense>

      <!-- Header with button -->
      <v-col cols="12" class="mb-4">
        <v-row class="align-center">
          <v-col cols="12" md="8" class="d-flex justify-center text-center text-md-start justify-md-start">
            <span class="text-h4 font-weight-bold">
              Zarządzaj wycieczkami
            </span>
          </v-col>
          <v-col cols="12" md="4" class="text-md-right text-start d-flex justify-center justify-md-end">
            <router-link :to="{ name: 'createTrip' }">
              <v-btn
                text="Dodaj wycieczkę"
                variant="outlined"
                rounded="lg"
                class="create-trip-button text-none"
              />
            </router-link>
          </v-col>
        </v-row>
      </v-col>

      <!-- Trip cards -->
      <v-col cols="12" md="6" v-for="trip in trips" :key="trip.id" class="pa-4">
        <v-card rounded="xl" elevation="4" class="trip-box">
          <v-row class="pa-4" align="center" justify="space-around" no-gutters>

            <!-- Image -->
            <v-col cols="12" sm="4" class="text-center pr-5">
              <v-img
                  :src="images.backgrounds.trip.img"
                  :alt="images.backgrounds.trip.alt"
                  class="trip-image"
                  aspect-ratio="1"
                  cover
              />
            </v-col>

            <!-- Trip Info -->
            <v-col cols="12" sm="7" md="8" lg="6">
              <v-row class="flex-column align-center">
                <v-card-title class="font-weight-bold pt-0">{{ trip.name }}</v-card-title>
                <v-card-subtitle class="font-weight-medium mb-2">
                  {{ formatDatePolish(trip.start_date) }} - {{ formatDatePolish(trip.end_date) }}
                </v-card-subtitle>

                <router-link :to="{ name: 'panel', params: { tripId: trip.id } }" class="w-100 mb-1">
                  <v-btn variant="flat" class="preview-trip-button text-white" block>
                    Zarządzaj wycieczką
                  </v-btn>
                </router-link>

                <router-link to="" class="w-100">
                  <v-btn variant="flat" class="delete-trip-button text-white" block>
                    Usuń wycieczkę
                  </v-btn>
                </router-link>
              </v-row>
            </v-col>

          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-col>
</template>


<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

.text-h4 {
  color: $primary-color;
}

.create-trip-button {
  border-color: $primary-color !important;
}

.trip-box {
  background-color: $background-secondary;
}

.preview-trip-button {
  background-color: $primary-color;
}

.delete-trip-button {
  background-color: $accent-color;
}

.trip-wrapper {
  max-width: 80%;
}

</style>
