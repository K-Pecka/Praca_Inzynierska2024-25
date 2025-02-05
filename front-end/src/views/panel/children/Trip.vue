<script lang="ts" setup>
import Box from "@/components/Box.vue";

const getTripTime = () => "12.12.2025 - 12.01.2026";
const getBudget = () => "12000 PLN";
const getParticipantCount = () => "0 Uczestników";
const getActivityCount = () => "28 Aktywności";
const getUpcomingActivities = () => [
  "18:30 - 19:30 Zbieranie truskawek",
  "20:00 - 23:00 Impreza",
];

const boxes = [
  {
    title: "Czas trwania",
    content: getTripTime,
    set: {
      order: 1,
      size: { sm: { col: 12, row: 1 }, md: { col: 6, row: 1 }, lg: { col: 3, row: 1 } },
    },
  },
  {
    title: "Budżet",
    content: getBudget,
    set: {
      order: 2,
      size: { sm: { col: 12, row: 1 }, md: { col: 6, row: 1 }, lg: { col: 3, row: 1 } },
    },
  },
  {
    title: "Uczestnicy",
    content: getParticipantCount,
    set: {
      order: 3,
      size: { sm: { col: 12, row: 1 }, md: { col: 6, row: 1 }, lg: { col: 3, row: 1 } },
    },
  },
  {
    title: "Aktywności",
    content: getActivityCount,
    set: {
      order: 4,
      size: { sm: { col: 12, row: 1 }, md: { col: 6, row: 1 }, lg: { col: 3, row: 1 } },
    },
  },
  {
    title: "Nadchodzące aktywności",
    content: getUpcomingActivities,
    set: {
      order: 5,
      size: { sm: { col: 12, row: 2 }, md: { col: 6, row: 2 }, lg: { col: 6, row: 2 } },
    },
  },
];
</script>

<template>
  <div class="grid-container">
    <template v-for="(box, index) in boxes" :key="index">
      <Box v-if="box?.title" :title="box.title" :content="box.content" :set="box.set" />
    </template>
  </div>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
}
</style>
