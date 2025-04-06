<script setup lang="ts">
import { useRoute } from "vue-router";
import {useTripStore} from "@/stores";

const route = useRoute();
const tripId = route.params.tripId as string;
const {getTripDetails} = useTripStore();
const {data: tripData, isLoading, error} = getTripDetails(tripId);
</script>
<template>
    <section class="section">
      <header class="section__title">
        <h1 class="trip-title" v-if="!isLoading && !error">{{ tripData?.name }}</h1>
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
  .section__title{
    margin: 0 0 3rem 0;
  }
  .section__subtitle{
    margin: 3rem 0 3rem 0;
  }
  .trip-title {
  font-size: 2rem;
  font-weight: 700;
  text-align: start;
  margin: 0 0 3rem 0;
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