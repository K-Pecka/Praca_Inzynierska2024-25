<script setup lang="ts">
import AppCard from "@/components/budget/AppCard.vue";
import AppButton from "@/components/budget/AppButton.vue";
import AppProgress from "@/components/budget/AppProgress.vue";
import ExpenseList from "@/components/budget/ExpenseList.vue";
import Section from "@/components/common/Section.vue";
import { ref } from "vue";
const budget = 1500;
const spent = 322;
const remaining = budget - spent;
const expenses = [
  {
    id: 1,
    title: "Tytuł",
    category: "jedzenie",
    date: "26.02.2025",
    amount: 322,
    notes: "Notatki bla bla",
  },
];
const categories = ref(["Jedzenie", "Transport", "Nocleg", "Rozrywka"]);
const participants = ref(["Jan", "Kasia", "Tomek"]);
</script>

<template>
  <Section>
    <template #title>
      <div class="d-flex justify-space-between align-center">
        <h1 class="title">Wydatki</h1>
        <AppButton class="add-button">Dodaj wydatek</AppButton>
      </div>
    </template>
    <template #content>
      <div class="summary">
        <AppCard class="summary-card">
          <h3>Budżet</h3>
          <p class="amount">{{ budget }} EUR</p>
        </AppCard>
        <AppCard class="summary-card">
          <h3>Wydano</h3>
          <AppProgress :value="spent" :max="budget" />
          <div class="d-flex justify-space-between" style="margin-top: 10%">
            <p class="spent">{{ spent }} EUR</p>
            <p class="percent">{{ ((spent / budget) * 100).toFixed(2) }}%</p>
          </div>
        </AppCard>
        <AppCard class="summary-card">
          <h3>Pozostało</h3>
          <p class="remaining">{{ remaining }} EUR</p>
        </AppCard>
      </div>

      <AppCard class="expenses">
        <v-card class="pa-4 mt-4 expenses-card">
          <div class="d-flex justify-space-between align-center">
            <h3 class="mb-2">Wydatki</h3>
            <div class="filters">
              <v-select label="Kategoria" :items="categories" variant="outlined"  class="filter-item"></v-select>
              <v-select label="Uczestnicy" :items="participants" variant="outlined" class="filter-item"></v-select>
              <v-text-field label="Data od" type="date" variant="outlined" class="filter-item"></v-text-field>
              <v-text-field label="Data do" type="date" variant="outlined" class="filter-item"></v-text-field>
            </div>
          </div>
        </v-card>

        <ExpenseList :expenses="expenses" />
      </AppCard>

      <div class="charts">
        <AppCard class="chart-card"
          ><h2 class="section-title">Wydatki - Kategorie</h2></AppCard
        >
        <AppCard class="chart-card"
          ><h2 class="section-title">Wydatki - Uczestnicy</h2></AppCard
        >
      </div>
    </template>
  </Section>
</template>

<style scoped lang="scss">
h1 {
  font-size: 2rem;
  text-align: start;
}
h3 {
  display: flex;
  font-size: 1.5rem;
}
.amount,
.remaining {
  font-size: 2.2rem;
}
.title {
  font-size: 26px;
  font-weight: bold;
  color: #333;
}
.add-button {
  background-color: #4a90e2;
  color: white;
  font-weight: bold;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
}

.summary {
  display: flex;
  gap: 8rem;
  justify-content: space-between;
  margin-bottom: 20px;
}
.expense-list {
  margin-top: 2rem;
}
.summary-card {
  background-color: #f3f3ff;
  padding: 16px;
  border-radius: 12px;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.amount {
  font-weight: bold;
  color: #333;
}
.spent {
  font-size: 1.125rem;
  color: #4a90e2;
  font-weight: bold;
}
.remaining {
  color: #2e7d32;
  font-weight: bold;
}

.expenses {
  background-color: #ede9fe;
  padding: 20px;
  margin-top: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.filters {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
.filter-item {
  width: 10vw;
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  color: #444;
  margin-bottom: 10px;
}

.charts {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  margin-top: 20px;
}

.chart-card {
  flex: 1;
  background-color: #f8f8ff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.filter-item :deep(.v-input__control){
  border-radius: 0.5rem;
}
@media (min-width: 600px) {
  .summary {
    gap: 1rem;
  }
  h3{
    font-size: 1.2rem;
  }
  .spent{
    font-size: 1rem;
  }
  .amount,.remaining{
    font-size: 1.7rem;
  }
  .v-field__input,input{
    font-size: 1rem;
  }
}
</style>
