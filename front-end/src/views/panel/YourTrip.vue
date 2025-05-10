<script setup lang="ts">
import { useTripStore, useUtilsStore, useAuthStore } from "@/stores";
import AppButton from "@/components/AppButton.vue";
import Loader from "@/components/common/AppLoader.vue"
import {images} from "@/data";
useTripStore().initialize();
const {userData} = useAuthStore();
const {isOwner} =userData;
const {formatDatePolish} = useUtilsStore()
const {trip} = useTripStore();
const {getTrips,deleteTrip} = trip
const {trips, isLoading_trips} = getTrips();
</script>

<template>
  <v-col cols="12" sm="10" md="10" lg="10" xl="10">

    <!-- Header with button -->
    <v-row
        no-gutters
        class="justify-space-between align-center mb-10"
    >
        <span class="text-h4 pb-4 font-weight-bold">
          Zarządzaj wycieczkami
        </span>
      <router-link :to="{ name: 'createTrip' }">

        <AppButton
            color="empty"
            height-auto
            font-auto
            text="Dodaj wycieczkę"
        />
      </router-link>
    </v-row>
    <v-row v-if="isLoading_trips">
      <Loader text="Ładowanie danych..." />
    </v-row>
    <!-- Trip cards -->
    <v-row v-else-if="trips">
      <v-col
          v-if="trips.length > 0"
          v-for="trip in trips" :key="trip.id"
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
                <v-card-title class="font-weight-bold">{{ trip.name }}</v-card-title>
                <v-card-subtitle class="font-weight-medium pb-6">
                  {{ formatDatePolish(trip.start_date) }} - {{ formatDatePolish(trip.end_date) }}
                </v-card-subtitle>
                
                <!-- Buttons -->
                <AppButton
                    :to="{ name: 'panel', params: { tripId: trip.id} }"
                    color="primary"
                    height-auto
                    stretch
                    :text="isOwner(trip.creator.id) ? 'Zarządzaj wycieczką' : 'Podgląd wycieczki'"
                />

                <v-card-subtitle
                  v-if="!isOwner(trip.creator.id)"
                  class="text-subtitle-2 d-flex align-center text-grey-2 pt-4"
                >
                  <v-icon size="18" class="mr-1" color="text-grey-2">mdi-account</v-icon>
                  {{ trip.creator.first_name }} {{ trip.creator.last_name }}
                </v-card-subtitle>

                <AppButton
                    v-else
                    to=""
                    color="accent"
                    height-auto
                    stretch
                    text="Usuń wycieczkę"
                    :onClick=" ()=> deleteTrip.mutate({tripId:String(trip.id)})"
                />

              </v-card-actions>
            </v-row>
          </v-card-text>
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
                color="secondary"
                text="Dodaj wycieczkę"
            />
          </router-link>
        </v-row>
      </v-col>
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
