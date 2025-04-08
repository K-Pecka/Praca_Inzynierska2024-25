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
import HeaderSection from "@/components/common/HeaderSection.vue";
</script>

<template>
  <Section>
    <template #title>
      <div class="title-container">
        <HeaderSection>
        <template #subtitle>
          <div class="title-container pb-4">
            <h2 class="trip-title">Wydatki</h2>
            <AppButton class="add-button">Dodaj wydatek</AppButton>
          </div>
        </template>
      </HeaderSection>
      </div>
      
    </template>
    <template #content>
      <v-container>
        <v-row>
          <v-col class="pr-sm-3" col="12" md="4">
            <AppCard>
              <h3>Budżet</h3>
              <p class="amount">{{ budget }} EUR</p>
            </AppCard>
          </v-col>
          <v-col class="px-sm-3" col="12" md="4">
            <AppCard class="summary-card">
              <h3>Wydano</h3>
              <AppProgress :value="spent" :max="budget" />
              <div class="d-flex justify-space-between" style="margin-top: 10%">
                <p class="spent">{{ spent }} EUR</p>
                <p class="percent">
                  {{ ((spent / budget) * 100).toFixed(2) }}%
                </p>
              </div>
            </AppCard>
          </v-col>
          <v-col class="pl-sm-3" col="12" md="4">
            <AppCard class="summary-card">
              <h3>Pozostało</h3>
              <p class="remaining">{{ remaining }} EUR</p>
            </AppCard>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <AppCard class="expenses">
              <div class="d-flex justify-space-between align-center">
                <h3 class="mb-2">Wydatki</h3>
                <div class="filters">
                  <v-select
                    bg-color="background"
                    label="Kategoria"
                    :items="categories"
                    variant="outlined"
                    class="filter-item"
                  ></v-select>
                  <v-select
                    bg-color="background"
                    label="Uczestnicy"
                    :items="participants"
                    variant="outlined"
                    class="filter-item"
                  ></v-select>
                  <v-text-field
                    bg-color="background"
                    label="Data od"
                    type="date"
                    variant="outlined"
                    class="filter-item"
                  ></v-text-field>
                  <v-text-field
                    bg-color="background"
                    label="Data do"
                    type="date"
                    variant="outlined"
                    class="filter-item"
                  ></v-text-field>
                </div>
              </div>

              <ExpenseList :expenses="expenses" />
            </AppCard>
          </v-col>
        </v-row>
        <v-row class="pt-6">
          <v-col>
            <AppCard class="chart-card"
              ><h2 class="section-title">Wydatki - Kategorie</h2></AppCard
            >
          </v-col>
          <v-col>
            <AppCard class="chart-card"
              ><h2 class="section-title">Wydatki - Uczestnicy</h2></AppCard
            >
          </v-col>
        </v-row>
      </v-container>
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
}
.add-button {
  background-color: #4a90e2;
  color: white;
  font-weight: bold;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
}

.expense-list {
  margin-top: 2rem;
}

.amount {
  font-weight: bold;
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
  padding: 20px;
  margin-top: 2rem;
  border-radius: 12px;
}

.filters {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.filter-item :deep(.v-input__control) {
  border-radius: 0.5rem;
}
@media (min-width: 600px) {
  h3 {
    font-size: 1.2rem;
  }
  .spent {
    font-size: 1rem;
  }
  .amount,
  .remaining {
    font-size: 1.7rem;
  }
  .v-field__input,
  input {
    font-size: 1rem;
  }
}
</style>
