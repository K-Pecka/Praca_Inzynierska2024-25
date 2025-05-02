<script setup lang="ts">
import {useTripStore} from "@/stores/trip/useTripStore";
import {useRoute} from "vue-router";
import AppButton from "@/components/budget/AppButton.vue";
import {useUtilsStore} from "@/stores";
import {images} from "@/data";

useTripStore().initialize(useRoute().name as string);

const {yourTrips} = useTripStore();
const {data: trips} = yourTrips.trips()
const {formatDatePolish} = useUtilsStore();

</script>

<template>
  <v-col cols="12">
    <v-row class="trip-wrapper mx-auto w-100" dense>

      <!-- Header with button -->
      <v-col v-if="trips && trips.length" cols="12" class="mb-4">
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
      <v-col v-if="trips && trips.length" cols="12" md="6" v-for="trip in trips" :key="trip.id" class="pa-4">
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
            <v-col cols="auto">
              <v-row class="flex-column align-center">
                <v-card-title class="font-weight-bold pt-0">{{ trip.name }}</v-card-title>
                <v-card-subtitle class="font-weight-medium pb-6">
                  {{ formatDatePolish(trip.start_date) }} - {{ formatDatePolish(trip.end_date) }}
                </v-card-subtitle>

                <AppButton
                    :to="{ name: 'panel', params: { tripId: trip.id } }"
                    class="trip-button w-100 mb-1"
                    variant="primary"
                >
                  Zarządzaj wycieczką
                </AppButton>

                <AppButton
                    to=""
                    class="trip-button w-100"
                    variant="accent"
                >
                  Usuń wycieczkę
                </AppButton>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- Empty state -->
      <v-col v-else cols="12" class="text-center py-10">
        <v-row class="flex-column">
          <span class="empty-header font-weight-bold mb-8">
              Nie masz jeszcze żadnych wycieczek
          </span>
          <v-img
              :src="images.emptyState.trip.img"
              :alt="images.emptyState.trip.alt"
              class="empty-trip-image mx-auto"
              aspect-ratio="1"
              contain
          />
          <router-link :to="{ name: 'createTrip' }">
            <AppButton
                variant="secondary"
                class="trip-button"
            >
              Dodaj wycieczkę
            </AppButton>
          </router-link>
        </v-row>
      </v-col>
    </v-row>
  </v-col>
</template>


<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

.text-h4 {
  color: $primary-color;
}

.trip-button {
  font-size: clamp(0.4em, 0.6vw + 0.45em, 1em);
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

.empty-header {
  font-size: clamp(0.9em, 1.5vw + 0.8em, 2.3em);
  color: $primary-color;
}

.empty-trip-image {
  width: clamp(15em, 15vw + 10em, 30em);
  height: auto;
}
</style>
