<script setup lang="ts">
import {useTripStore, useUtilsStore, useAuthStore} from "@/stores";
import {useSafeDelete} from "@/composables/useSafeDelete";
import AppButton from "@/components/AppButton.vue";
import Loader from "@/components/shared/AppLoader.vue"
import {images} from "@/data";
import {Trip} from "@/types";
import { useRoute } from "vue-router";
const {confirmAndRun} = useSafeDelete();
const tripStore = useTripStore();
tripStore.initialize();
const {trip} = tripStore;
const {userData} = useAuthStore();
const {isOwner} = userData;
const {formatDatePolish} = useUtilsStore()
const {getTrips, deleteTrip} = trip
const {trips, isLoading_trips} = getTrips();

const isTripOwner = (trip: Trip) => isOwner(trip.creator.id);

const handleDelete = (tripId: string) => {
  confirmAndRun(() => {
    deleteTrip.mutate({ tripId });
  }, {
    title: "Potwierdź usunięcie wycieczki",
    message: "Czy na pewno chcesz usunąć tę wycieczkę? Tego działania nie można cofnąć.",
    wordToConfirm: "USUŃ"
  });
};

import { HeaderSection } from "@/components";

const route = useRoute();

</script>

<template>
  <v-col cols="12" sm="10" md="10" lg="10" xl="10">
    <HeaderSection
        title="Zarządzaj wycieczkami"
        subtitle="Przeglądaj i zarządzaj swoimi wycieczkami"
        :button="true"
        buttonText="Dodaj wycieczkę"
        btnGoBack
        :buttonAction="() => $router.push({ name: 'createTrip', params:{role:route.params.role} })"
        :goBackAction="() => $router.push({ name: 'roleSelection' })"
      />
    <!-- Header with button -->
    <v-row v-if="isLoading_trips">
      <Loader text="Ładowanie danych..."/>
    </v-row>
    <!-- Trip cards -->
    <v-row v-else>
      <template v-if="trips?.results && trips.results.length && trips.results.length > 0">
        <v-col
            v-for="trip in trips.results" :key="trip.id"
            cols="12"
            sm="6"
            md="4"
        >
          <v-card class="rounded-xl background-secondary d-flex justify-center">
            <v-card-text>
              <v-row no-gutters justify="space-around" align="center">

                <!-- Card image -->
                <v-img
                    :src="images.backgrounds.trip.img"
                    :alt="images.backgrounds.trip.alt"
                    aspect-ratio="1"
                    width="auto"
                    max-width="230px"
                />

                <!-- Trip Info -->
                <v-card-actions class="flex-column" style="max-width: 220px;">
                  <v-card-title class="font-weight-bold">{{trip.name }}</v-card-title>
                  <v-card-subtitle class="font-weight-medium pb-6">
                    {{ formatDatePolish(trip.start_date) || '' }} - {{ formatDatePolish(trip.end_date) || '' }}
                  </v-card-subtitle>

                  <!-- Buttons -->
                  <AppButton
                      :to="{ name: 'tripDashboard', params: { tripId: trip.id} }"
                      color="primary"
                      height-auto
                      stretch
                      :text="isTripOwner(trip) ? 'Zarządzaj wycieczką' : 'Podgląd wycieczki'"
                  />

                  <v-card-subtitle
                      v-if="!isTripOwner(trip)"
                      class="text-subtitle-2 d-flex align-center text-grey-2 pt-4"
                  >
                    <v-icon size="18" class="mr-1" color="text-grey-2">mdi-account</v-icon>
                    {{ trip.creator.first_name }} {{ trip.creator.last_name }}
                  </v-card-subtitle>

                  <AppButton
                      v-else
                      color="accent"
                      height-auto
                      stretch
                      text="Usuń wycieczkę"
                      :onClick="()=> handleDelete(String(trip.id))"
                  />

                </v-card-actions>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </template>
      <!-- Empty state -->
      <template v-else>
        <v-col cols="12" class="text-center py-10">
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
                  width="300px"
                  color="primary"
                  text="Dodaj wycieczkę"
              />
            </router-link>
          </v-row>
        </v-col>
      </template>
    </v-row>
  </v-col>
</template>


<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

.text-h4 {
  color: rgb($primary-color);
}

.empty-header {
  font-size: clamp(0.9em, 1.5vw + 0.8em, 2.3em);
  color: rgb($primary-color);
}

.empty-trip-image {
  width: clamp(15em, 15vw + 10em, 30em);
  height: auto;
}
</style>
