<script lang="ts" setup>
import {Box,Section} from "@/components";
import { useRoute } from "vue-router";
import { useTripStore } from "@/stores/trip/useTripStore";
const { getDashboard } = useTripStore();
const route = useRoute();
const id = route.params.tripId as string;

const { boxes, isLoading, error } = getDashboard(id);

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
            <Box :title="box.title" :content="box.content" :set="box.set" :icon="box.icon" />
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
  font-size: 2rem;
}
</style>
