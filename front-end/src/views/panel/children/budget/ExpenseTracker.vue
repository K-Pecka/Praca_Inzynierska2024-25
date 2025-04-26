<script setup lang="ts">
import AppCard from "@/components/budget/AppCard.vue";
import AppButton from "@/components/budget/AppButton.vue";
import AppProgress from "@/components/budget/AppProgress.vue";
import ExpenseList from "@/components/budget/ExpenseList.vue";
import Section from "@/components/common/Section.vue";
import { useUtilStore } from "@/stores";
import { useRoute } from "vue-router";
const route = useRoute();
const { mapCategoryBudget } = useUtilStore();
const id = route.params.tripId as string;
import { useTripStore } from "@/stores/trip/useTripStore";
const { getTripDetails,getExpensesQuery } = useTripStore();
import { computed, ref } from "vue";
const {data: tripRaw, isLoading, error} = getTripDetails(Number(id));
const {data: expenses} = getExpensesQuery(Number(id));

const budget = computed(() => Number(tripRaw.value?.budget?.amount) ?? 0);

const spent = computed(() =>{
  console.log("expenses", expenses.value);
  return expenses.value?.reduce((acc, expense) => Number(acc) + Number(expense.amount), 0) ?? 0;
});

const remaining = computed(() => Number(budget.value) - spent.value);

const categories = computed(() => {
  return [
    ...new Set(expenses.value?.map(expense => expense.category) ?? [])
  ]
  .map((categoryId) => {
    const category = mapCategoryBudget(categoryId);
    return {
      title: category.name,
      value: categoryId,
      icon: category.icon,
    };
  });
});
const participants = ref(["Jan", "Kasia", "Tomek"]);
import HeaderSection from "@/components/common/HeaderSection.vue";

const showForm = ref(true);
const showFilters = ref(false);

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
          <div class="title-container pb-4 w-100">
            <h2 class="trip-title mb-10" style="font-size: 30px; font-weight: 600; width: 80%;">Wydatki</h2>
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

              <ExpenseList variant="manage"/>  
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

      <v-dialog v-model="showFilters" max-width="500" >
        <v-card class="pa-3">
          <v-card-title class="text-h6">Filtry</v-card-title>
          <v-card-text>
            <v-container>
              <v-row dense>
                <v-col cols="12">
                  <v-select
                    v-model="selectedCategory"
                    :placeholder="selectedCategory || 'Wybierz kategorię'"
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
