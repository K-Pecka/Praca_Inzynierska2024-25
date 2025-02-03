<script lang="ts" setup>
import Box from "@/components/Box.vue"
const boxes = [
  {
    title: "Czas trwania",
    content: "12.12.2025 - 12.01.2026",
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
    content: "12000 PLN",
    set: {
      order: 2,
      size: {
        sm: { col: 12, row: 1 },
        md: { col: 6, row: 1 },
        lg: { col: 3, row: 1 },
      },
    },
  },,
  {
    title: "Uczestnicy",
    content: "0 Uczestników",
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
    content: "28 Aktywności",
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
    title: "Nadchdzące aktywności",
    content: ["18:30 - 19:30 Zbieranie trukawek","20:00 - 23:00 impreza"],
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
    title: "Nadchdzące aktywności",
    content: ["18:30 - 19:30 Zbieranie trukawek","20:00 - 23:00 impreza"],
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
    title: "Nadchdzące aktywności",
    content: ["18:30 - 19:30 Zbieranie trukawek","20:00 - 23:00 impreza"],
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
    title: "Nadchdzące aktywności",
    content: ["18:30 - 19:30 Zbieranie trukawek","20:00 - 23:00 impreza"],
    set: {
      order: 5,
      size: {
        sm: { col: 12, row: 2 },
        md: { col: 6, row: 2 },
        lg: { col: 6, row: 2 },
      },
    },
  }
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
