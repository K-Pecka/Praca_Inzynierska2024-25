<script setup lang="ts">
import {Section, TripCard} from "@/components";
import {useTripStore} from "@/stores/trip/useTripStore";
import HeaderSection from "@/components/common/HeaderSection.vue";
import AppButton from "@/components/AppButton.vue";
import {images} from "@/data";
import { useUtilsStore,useAuthStore } from "@/stores";
const {getTripId} = useUtilsStore();
const {plan} = useTripStore();
const {getPlans,planBtn} = plan;
const {plans,isLoading_plans,error_plans} = getPlans();

const {trip:tripStore} = useTripStore();
const {getTripDetails} = tripStore;
const {trip} = getTripDetails();

const { userData } = useAuthStore();
const { isOwner } = userData;

</script>

<template>

  <Section>
    <template #title v-if="trip && plans && plans.length">
      <HeaderSection subtitle="Plany podróży" />
    </template>
    <template #content>
      <template v-if="trip && plans && plans.length">
        <TripCard :plans="plans" :btn="planBtn ?? []" :isOwner = "isOwner(trip?.creator?.id)"/>
      </template>

      <!-- Empty state -->
      <template v-else>
        <v-col cols="12" class="text-center py-10">
          <v-row class="flex-column">
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
            <router-link :to="{ name: 'createPlan', params: { tripId: String(getTripId()) } }">
              <AppButton
                  color="secondary"
                  class="plan-button"
                  width="300px"
                  height="height-auto"
                  fontSize="font-auto"
                  text="Dodaj plan podróży"
              >
              </AppButton>
            </router-link>
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
