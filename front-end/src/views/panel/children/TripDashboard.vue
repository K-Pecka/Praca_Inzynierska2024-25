<script lang="ts" setup>
import Box from "@/components/Box.vue";
import { useRoute } from "vue-router";
import { useTripStore } from "@/stores/tripStore";
import { computed } from "vue";
import Section from "@/components/Section.vue";
const { getTripDetails } = useTripStore();
const route = useRoute();
const id = Number(route.params.tripId);

const { data: trip, isLoading, error } = getTripDetails(id);
console.log(trip);
const tripTime = computed(
  () => `${trip.value?.start_date ?? "..."} - ${trip.value?.end_date ?? "..."}`
);
const budget = computed(() => `${trip.value?.budget?.amount ?? "..."} PLN`);
const participantCount = computed(
  () => `${trip.value?.members.length ?? "..."} Uczestników`
);
const activityCount = computed(() => "0 Aktywności");
const upcomingActivities = computed(() => []);

const boxes = computed(() => [
  {
    title: "Czas trwania",
    content: tripTime.value,
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
    content: budget.value,
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
    content: participantCount.value,
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
    content: activityCount.value,
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
    content: upcomingActivities.value,
    set: {
      order: 5,
      size: {
        sm: { col: 12, row: 2 },
        md: { col: 6, row: 2 },
        lg: { col: 6, row: 2 },
      },
    },
  },
  {
    title: "Ważne informacje",
    content: upcomingActivities.value,
    set: {
      order: 5,
      size: {
        sm: { col: 12, row: 2 },
        md: { col: 6, row: 2 },
        lg: { col: 6, row: 2 },
      },
    },
  },
]);
</script>

<template>
    <template v-if="isLoading">
      <div class="grid-container">
        <Box
        title="Ładowanie..."
        content="Pobieranie danych..."
        :set="{
          order: 1,
          size: {
            sm: { col: 12, row: 4 },
            md: { col: 12, row: 4 },
            lg: { col: 12, row: 4 },
          },
        }"
      />
      </div>
    </template>
    <template v-else-if="error">
      <div class="grid-container">
      <Box
        title="Błąd"
        :content="`Błąd: ${error.message}`"
        :set="{
          order: 1,
          size: {
            sm: { col: 12, row: 4 },
            md: { col: 12, row: 4 },
            lg: { col: 12, row: 4 },
          },
        }"
      />
      </div>
    </template>
    <template v-else>
      <Section>
        <template #title>
          <h1>Wakacje we Francji</h1>
        </template>

        <template #content>
          <div class="grid-container">
            <template v-for="(box, index) in boxes" :key="index">
            <Box :title="box.title" :content="box.content" :set="box.set" />
          </template>
          </div>
          
        </template>
      </Section>
    </template>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 2rem;
  height: 100%;
  font-size: 2rem;
}
h1 {
  text-align: start;
}
</style>
