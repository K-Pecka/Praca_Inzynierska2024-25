<script setup lang="ts">
import {useRoute} from "vue-router";
import {useTripStore} from "@/stores";

const route = useRoute();
const tripId = Number(route.params.tripId);
const {getTripDetails} = useTripStore();
const {data: tripData, isLoading, error} = getTripDetails(tripId);
</script>
<template>
  <section class="section">
    <header class="section__title">
      <h1 class="trip-title mt-10" v-if="!isLoading && !error">{{ tripData?.name }}</h1>
      <h1 class="trip-title" v-else>...</h1>
    </header>
    <div class="section__subtitle">
      <slot name="subtitle"></slot>
    </div>
  </section>
</template>
<style scoped lang="scss">
* {
  width: 100%;
  text-align: start;
}

.section__title {
  margin: 0 0 2rem 0;
  display: flex;
}

.section__subtitle {
  margin: 2rem 0 2rem 0;
  color: rgb(var(--v-theme-text), 0.75);
  display: flex;
}

.trip-title {
  font-family: var(--v-fontFamily);
  font-size: 2rem;
  width: 80%;
  font-weight: 700;
  color: rgb(var(--v-theme-text), 0.75);
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.title-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}


</style>