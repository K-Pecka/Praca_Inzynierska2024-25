<script lang="ts" setup>
import { Box, Section } from "@/components";
import { useRoute } from "vue-router";
import { useTripStore } from "@/stores/trip/useTripStore";
import { Expense } from "@/type";
import ExpenseList from "@/components/expenseItem/ExpenseList.vue";
import HeaderSection from "@/components/common/HeaderSection.vue";
const { getDashboard } = useTripStore();
const route = useRoute();
const id = route.params.tripId as string;

const { boxes, isLoading, error, tripName } = getDashboard(id);

const expenseItem: Expense[] = [
  {
    title: "test",
    date: "12-02-2022",
    type: "food",
    note: "bla bla bla",
    amount: 100,
    currency: "PLN",
  },
  {
    title: "test",
    date: "12-02-2022",
    type: "food",
    note: "bla bla bla",
    amount: 100,
    currency: "PLN",
  },
];
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
        <HeaderSection>
              <template #subtitle>
                 <h2 class="trip-title">Panel</h2>
              </template>
              </HeaderSection>
      </template>

      <template #content>
        <div class="grid-container">
          <template v-for="(box, index) in boxes" :key="index">
            <Box
              :title="box.title"
              :content="box.content"
              :set="box.set"
              :icon="box.icon"
            />
          </template>
          
        </div>
        <v-card class="dashboard-card" elevation="3">
          <v-card-title class="text-h6 font-weight-medium d-flex align-center">
            Ostatnie wydatki
          </v-card-title>
            <ExpenseList :expenses="expenseItem" />
          </v-card>
      </template>
    </Section>
  </template>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
  font-size: 2rem;
}
h1 {
  text-align: start;
  font-size: 2rem;
}
.dashboard-card {
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: rgb(var(--v-theme-secondary), 50%);
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 2rem;
}
.v-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}
</style>
