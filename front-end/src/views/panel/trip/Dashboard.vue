<script lang="ts" setup>
import { Box, Section, HeaderSection,ExpensesList } from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
useTripStore().initialize();
const { dashboard, budget } = useTripStore();
const { getDashboard, getSpecialSectionName } = dashboard;
const { getExpensByTrip } = budget;

const { boxes, isLoading_trip, error_trip } = getDashboard();
const { expensesByTrip, isLoading_expenses } = getExpensByTrip();
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection subtitle="Panel" />
    </template>
    <template #content>
      <!-- Loadder -->
      <template v-if="isLoading_trip"> Loading... </template>
      <template v-else-if="error_trip">Error ... </template>
      <template v-else>
        <div class="grid-container w-100">
          <template v-for="(box, index) in boxes" :key="index">
            <Box
              :title="box.title"
              :content="box.content"
              :set="box.set"
              :icon="box.icon"
            />
          </template>
        </div>
        <v-card class="dashboard-card w-100" elevation="3">
          <v-card-title
            class="text-h6 pt-0 font-weight-bold expense-card-title"
          >
            {{ getSpecialSectionName() }}
          </v-card-title>
          <!-- Loadder -->
          <template v-if="isLoading_expenses"> Loading expenses... </template> 
          <ExpensesList
            v-else
            variant="view"
            :limit="4"
            :expenses="expensesByTrip"
          />
        </v-card>
      </template>
    </template>
  </Section>
</template>

<style scoped lang="scss">
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
