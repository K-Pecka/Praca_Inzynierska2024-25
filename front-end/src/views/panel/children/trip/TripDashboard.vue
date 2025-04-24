<script lang="ts" setup>
import { Box, Section } from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import { Expense } from "@/types";
import ExpenseList from "@/components/expenseItem/ExpenseList.vue";
import HeaderSection from "@/components/common/HeaderSection.vue";
import { useRoute } from "vue-router";

useTripStore().initialize(useRoute().name as string);
const { getDashboard,getExpenseItem } = useTripStore();

const route = useRoute();
const id = route.params.tripId as string;

const { boxes, isLoading, error, tripName } = getDashboard(id);

const expenseItem: Expense[] = getExpenseItem().expenseItem;
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection>
        <template #subtitle>
          <h2 class="trip-title mb-10" style="font-size: 30px; font-weight: 600; width: 80%;">Panel</h2>
        </template>
      </HeaderSection>
    </template>
    <template #content>
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
        <div class="grid-container" style="width: 80%;">
          <template v-for="(box, index) in boxes" :key="index">
            <Box
              :title="box.title"
              :content="box.content"
              :set="box.set"
              :icon="box.icon"
            />
          </template>
        </div>
        <v-card class="dashboard-card" elevation="3" style="width: 80%;">
          <v-card-title class="text-h6 pt-0 font-weight-bold expense-card-title">
            {{getExpenseItem().sectionName}}
          </v-card-title>
          <ExpenseList :expenses="expenseItem" />
        </v-card>
      </template>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.expense-card-title {
  font-family: var(--v-fontFamily);
}
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
