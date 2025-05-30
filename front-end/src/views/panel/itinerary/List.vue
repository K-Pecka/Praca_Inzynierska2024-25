<script setup lang="ts">
import {Section, ItineraryCard} from "@/components";
import {useTripStore} from "@/stores/trip/useTripStore";
import HeaderSection from "@/components/shared/HeaderSection.vue";
import AppButton from "@/components/AppButton.vue";
import {images} from "@/data";
import { useUtilsStore,useAuthStore } from "@/stores";
import { useRouter } from "vue-router";
import { computed } from "vue";
const {getTripId} = useUtilsStore();
const {itinerary} = useTripStore();
const {getItineraries} = itinerary;
const {itineraries, isLoading_itineraries, error_itineraries} = getItineraries();

const itineraryWithActivities= computed(() => itineraries.value?.results.filter(el =>isOwner(trip.value?.creator?.id ?? 0) || el && typeof el.activities_count === 'number' && el.activities_count > 0))
const {trip:tripStore} = useTripStore();
const {getTripDetails} = tripStore;
const {trip} = getTripDetails();

const { userData } = useAuthStore();
const { isOwner } = userData;
const router = useRouter();
const goToCreateItinerary= () => {
  if (isOwner(trip.value?.creator?.id ?? 0)) {
    router.push({ name: 'createItinerary', params: { tripId: String(getTripId()) } });
  }
}
</script>

<template>

  <Section>
    <template #title v-if="trip && itineraries && itineraries.results.length">
      <HeaderSection subtitle="Plany podróży" />
    </template>
    <template #content>
      <p v-if="isLoading_itineraries">Ładowanie...</p>
      <p v-else-if="error_itineraries">Błąd: {{ error_itineraries.message }}</p>
      <template v-else-if="trip && itineraries && itineraries.results.length">
        <ItineraryCard
            :itineraries="itineraryWithActivities"
            :isOwner = "isOwner(trip?.creator?.id)"
        />
      </template>

      <!-- Empty state -->
      <template v-if="itineraries && itineraries?.results.length==0">
        <v-col cols="12" class="text-center py-10">
          <v-row class="flex-column align-center">
          <span class="empty-header font-weight-bold mb-8">
              Nie masz jeszcze żadnych planów podróży
          </span>
            <v-img
                :src="images.emptyState.plan.img"
                :alt="images.emptyState.plan.alt"
                class="empty-plan-image mx-auto"
                aspect-ratio="1"
                contain
            />
            <AppButton
                color="primary"
                class="plan-button"
                width="300px"
                height="height-auto"
                fontSize="font-auto"
                text="Dodaj plan podróży"
                :disabled="!isOwner(trip?.creator?.id ?? 0)"
                @click="goToCreateItinerary"
              />
          </v-row>
        </v-col>
      </template>
    </template>
  </Section>
</template>

<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

.empty-header {
  font-size: clamp(0.3em, 1.5vw + 0.5em, 1.5em);
  color: rgb($primary-color);
}

.empty-plan-image {
  width: clamp(15em, 15vw + 10em, 25em);
  height: auto;
}

</style>
