<script setup lang="ts">
import {Section,TripBox} from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import { useRoute } from "vue-router";
useTripStore().initialize(useRoute().name as string);
const { yourTrips } = useTripStore();
const { data: trips, isLoading, error, isSuccess } = yourTrips.trips()
</script>

<template>
  <v-container fluid class="full-width-container">
    <v-row>
      <v-col cols="12" md="10" offset-md="1">
        <Section>
          <template #title>
            <div class="d-flex justify-between align-center justify-space-between">
              <h1 class="mr-1">Zarządzaj wycieczkami</h1>
              <router-link :to="{name: 'TripForm'}">
                 <v-btn  outlined class="text-primary p-5">
                  Dodaj
                </v-btn>
                <!--BaseButton variant="secondary" size="small">Dodaj wycieczkę</!--BaseButton-->
              </router-link>
             
            </div>
            
            <RouterLink to="/"></RouterLink>
          </template>
          <template #content>
            <p v-if="isLoading">Ładowanie...</p>
            <p v-else-if="error">Błąd: {{ error.message }}</p>
            <TripBox v-else-if="trips && trips.length > 0" :btn="yourTrips.btn.map(btn => ({ ...btn, onclick: async (id: string) => { await btn.onclick(id); return; } }))" :trip="trips" image="/picture/p1.svg" />
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
  @media (max-width: 600px) {
        font-size: 1.5rem;
      }
}
.v-btn{
  font-weight: bold;
  border:2px solid rgb(var(--v-theme-primary));
}
</style>
