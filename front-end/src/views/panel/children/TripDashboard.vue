<script lang="ts" setup>
import Box from "@/components/Box.vue";
import { useRoute } from "vue-router";
import { useTripStore } from "@/stores/tripStore";

const { getTripDetails } = useTripStore();

const route = useRoute();
const id = Number(route.params.id);

const { data: trip, isLoading, error, isSuccess } = getTripDetails(id);

const getTripTime = (id: Number) =>
  `${trip.value?.start_date} - ${trip.value?.end_date}`;
const getBudget = (id: Number) => `${trip.value?.budget} PLN`;
const getParticipantCount = (id: Number) =>
  `${trip.value?.members} Uczestników`;
const getActivityCount = (id: Number) => "28 Aktywności";
const getUpcomingActivities = (id: Number) => [
  "18:30 - 19:30 Zbieranie truskawek",
  "20:00 - 23:00 Impreza",
];
const boxes = [
  {
    title: "Czas trwania",
    content: (id: Number) => getTripTime(id),
    set: {
      order: 1,
      size: {
        sm: { col: 12, row: 1 },
        md: { col: 6, row: 1 },
        lg: { col: 3, row: 1 },
      },
    },
  },
  {
    title: "Budżet",
    content: (id: Number) => getBudget(id),
    set: {
      order: 2,
      size: {
        sm: { col: 12, row: 1 },
        md: { col: 6, row: 1 },
        lg: { col: 3, row: 1 },
      },
    },
  },
  {
    title: "Uczestnicy",
    content: (id: Number) => getParticipantCount(id),
    set: {
      order: 3,
      size: {
        sm: { col: 12, row: 1 },
        md: { col: 6, row: 1 },
        lg: { col: 3, row: 1 },
      },
    },
  },
  {
    title: "Aktywności",
    content: (id: Number) => getActivityCount(id),
    set: {
      order: 4,
      size: {
        sm: { col: 12, row: 1 },
        md: { col: 6, row: 1 },
        lg: { col: 3, row: 1 },
      },
    },
  },
  {
    title: "Nadchodzące aktywności",
    content: (id: Number) => getUpcomingActivities(id),
    set: {
      order: 5,
      size: {
        sm: { col: 12, row: 2 },
        md: { col: 6, row: 2 },
        lg: { col: 6, row: 2 },
      },
    },
  },
];
</script>

<template>
  <div class="grid-container">
    <template v-if="isLoading">
      <Box
        title="loading..."
        :content="() => 'Pobieranie danych'"
        :set="{
        order: 1,
        size: {
          sm: { col: 12, row: 4 },
          md: { col: 12, row: 4 },
          lg: { col: 12, row: 4 },
        },
      }"
      />
    </template>
    <template v-else-if="error">
      <Box
        title="Error"
        :content="() => `Błąd: ${error.message}`"
        :set="{
        order: 1,
        size: {
          sm: { col: 12, row: 4 },
          md: { col: 12, row: 4 },
          lg: { col: 12, row: 4 },
        },
      }"
      />
    </template>
    <template v-else>
      <template v-for="(box, index) in boxes" :key="index">
      <Box
        v-if="box?.title"
        :title="box.title"
        :content="box.content"
        :set="box.set"
        :id="id"
        :isLoading="isLoading"
        :error="error"
      />
    </template>
    
    </template>
  </div>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
  height: 100%;
}
</style>
