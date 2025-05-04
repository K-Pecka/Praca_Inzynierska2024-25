<script setup lang="ts">
import {Section,TripBox} from "@/components";
import { images } from "@/data";
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
            <div class="d-flex justify-between align-center justify-space-between mt-15" style="width: 100%;">
              <h1 class="mr-1 pb-4">Zarządzaj wycieczkami</h1>
              <router-link :to="{name: 'TripForm'}">
                 <v-btn  outlined class="text-primary p-5" style="text-transform: none; border-radius: 8px;">
                  Dodaj wycieczkę
                </v-btn>
              </router-link>
             
            </div>
            
            <RouterLink to="/"></RouterLink>
          </template>
          <template #content>
            <p v-if="isLoading">Ładowanie...</p>
            <p v-else-if="error">Błąd: {{ error.message }}</p>
            <TripBox v-else-if="trips && trips.length > 0" :btn="yourTrips.btn.map(btn => ({ ...btn, onclick: async (id: string) => { await btn.onclick(id); return; } }))" :trip="trips" :image="images.backgrounds.trip" />
          </template>
        </Section>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
@media (min-width: 960px) {
.v-col-md-10 {
  max-width: 100rem;
  margin-left: auto;
  margin-right: auto;
  justify-content: center;
}
}
h1 {
  font-size: 2.25rem;
  text-align: left;
}
.v-btn{
  font-weight: bold;
  border:2px solid rgb(var(--v-theme-primary));
}
</style>
