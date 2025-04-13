<!-- <script setup lang="ts">
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
const showForm = ref(true);
</script>

<template>
  <Section>
    <template #title>
        <HeaderSection>
        <template #subtitle>
          <div class="title-container pb-4">
            <h2 class="section-title">Wydatki</h2>
            <AppButton
                    variant="primary"
                    size="md"
                    @click="showForm = !showForm"
                  >
                    <v-icon v-if="$vuetify.display.smAndDown">mdi-plus</v-icon>
                    <span v-else>Dodaj</span>
                  </AppButton>
          </div>
        </template>
      </HeaderSection>
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
.title-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
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
</style> -->

<script setup lang="ts">
import AppCard from "@/components/budget/AppCard.vue";
import AppButton from "@/components/budget/AppButton.vue";
import AppProgress from "@/components/budget/AppProgress.vue";
import ExpenseList from "@/components/budget/ExpenseList.vue";
import Section from "@/components/common/Section.vue";
import HeaderSection from "@/components/common/HeaderSection.vue";
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

const showForm = ref(true);
const showFilters = ref(false);

// wartości filtrów (opcjonalnie do podpięcia logiki filtrowania)
const selectedCategory = ref<string | null>(null);
const selectedParticipant = ref<string | null>(null);
const dateFrom = ref<string | null>(null);
const dateTo = ref<string | null>(null);
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection>
        <template #subtitle>
          <div class="title-container pb-4">
            <h2 class="section-title">Wydatki</h2>
            <div class="d-flex">
              <AppButton
                variant="primary"
                size="md"
                @click="showForm = !showForm"
              >
                <v-icon v-if="$vuetify.display.smAndDown">mdi-plus</v-icon>
                <span v-else>Dodaj</span>
              </AppButton>
            </div>
          </div>
        </template>
      </HeaderSection>
    </template>

    <template #content>
      <v-container fluid>
        <v-row>
          <v-col col="12" sm="12" md="4" order="1" order-md="1">
            <AppCard class="summary-card ml-md-0">
              <h3>Budżet</h3>
              <p class="amount">{{ budget }} EUR</p>
            </AppCard>
          </v-col>
          <v-col col="12" sm="12" md="4" order="3" order-md="2">
            <AppCard class="summary-card" >
              <h3>Wydano</h3>
              <AppProgress :value="spent" :max="budget" />
              <div class="d-flex justify-space-between mt-4">
                <p class="spent">{{ spent }} EUR</p>
                <p class="percent">
                  {{ ((spent / budget) * 100).toFixed(2) }}%
                </p>
              </div>
            </AppCard>
          </v-col>
          <v-col col="12" sm="12" md="4" order="2" order-md="3">
            <AppCard class="summary-card mr-md-0">
              <h3>Pozostało</h3>
              <p class="remaining">{{ remaining }} EUR</p>
            </AppCard>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <AppCard class="expenses">
              <div class="title-container pb-4">
                <h3 class="mb-2">Wydatki</h3>

                <AppButton
                  variant="primary"
                  size="md"
                  @click="showFilters = true"
                >
                  <v-icon start>mdi-filter</v-icon>
                  Filtruj
                </AppButton>
              </div>

              <ExpenseList :expenses="expenses" />
            </AppCard>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <AppCard class="chart-card ml-0">
              <h2 class="section-title ">Wydatki - Kategorie</h2>
            </AppCard>
          </v-col>
          <v-col>
            <AppCard class="chart-card mr-0">
              <h2 class="section-title ">Wydatki - Uczestnicy</h2>
            </AppCard>
          </v-col>
        </v-row>
      </v-container>

      <!-- FILTRY W DIALOGU -->
      <v-dialog v-model="showFilters" max-width="500" >
        <v-card class="pa-3">
          <v-card-title class="text-h6">Filtry</v-card-title>
          <v-card-text>
            <v-container>
              <v-row dense>
                <v-col cols="12">
                  <v-select
                    v-model="selectedCategory"
                    :items="categories"
                    label="Kategoria"
                    variant="outlined"
                  />
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="selectedParticipant"
                    :items="participants"
                    label="Uczestnik"
                    variant="outlined"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="dateFrom"
                    label="Data od"
                    type="date"
                    variant="outlined"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="dateTo"
                    label="Data do"
                    type="date"
                    variant="outlined"
                  />
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn text @click="showFilters = false">Anuluj</v-btn>
            <v-btn color="primary" @click="showFilters = false">Zastosuj</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.title-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
h3 {
  font-size: 1.5rem;
}
.amount,
.remaining {
  font-size: 2.2rem;
  font-weight: bold;
}
.spent {
  font-size: 1.125rem;
  color: #4a90e2;
  font-weight: bold;
}
.remaining {
  color: #2e7d32;
}
.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}
.expenses {
  padding: 20px;
  margin-top: 2rem;
  border-radius: 12px;
}
.summary-card{
  width: 95%;
  margin:auto;
}
.chart-card{
  width: 97%;
  margin:auto;
}
.v-col{
  margin: 0.5rem 0;
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
