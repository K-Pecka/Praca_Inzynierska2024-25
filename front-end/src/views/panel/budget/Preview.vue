<script setup lang="ts">
import {
  ExpensesList,
  Section,
  HeaderSection,
  ExpenseForm,
  BudgetContent,
  AppButton,
  AppCard,
} from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import { budget as budgetCategory } from "@/data/category/budget";
import { computed, ref } from "vue";
import { useMembersStore } from "@/stores/trip/useMembersStore";
import { Expense } from "@/types";
import { VDateInput } from "vuetify/labs/components";
import dayjs from "dayjs";
import { useAuthStore, useUtilsStore } from "@/stores";

const { members: membersStore } = useMembersStore();
const members = computed(() => membersStore);
const { budget: budgetStore, trip: tripStore } = useTripStore();
const { getExpensByTrip } = budgetStore;

const onExpenseAdded = () => {
  showForm.value = false;
};

const { getTripDetails } = tripStore;
const { trip } = getTripDetails();
const { expensesByTrip: expenses } = getExpensByTrip();
const budget = computed(() => Number(trip.value?.budget_amount) ?? 0);
const budgetCurrency = computed(() => "PLN");

const spent = computed(() => {
  return (
    expenses.value?.reduce(
      (acc, expense) => Number(acc) + Number(expense.converted_amount),
      0
    ) ?? 0
  );
});

const remaining = computed(() => Number(budget.value) - spent.value);

const showForm = ref(false);
const showFilters = ref(false);

const selectedCategory = ref<string | null>(null);
const selectedParticipant = ref<string | null>(null);
const dateFrom = ref<string | null>(null);
const dateTo = ref<string | null>(null);

const appliedFilters = ref<{
  category: string | null;
  participants: string | null;
  dateFrom: string | null;
  dateTo: string | null;
}>({
  category: null,
  participants: null,
  dateFrom: null,
  dateTo: null,
});

const toggleForm = () => {
  showForm.value = !showForm.value;
};

const filter = () => {
  appliedFilters.value = {
    category: selectedCategory.value,
    participants: selectedParticipant.value,
    dateFrom:
      dateFrom.value == null
        ? dayjs().format("DD.MM.YYYY")
        : dayjs(dateFrom.value).format("DD.MM.YYYY"),
    dateTo:
      dateTo.value == null
        ? dayjs().format("DD.MM.YYYY")
        : dayjs(dateTo.value).format("DD.MM.YYYY"),
  };
  showFilters.value = false;
};
const { mapCategoryBudget } = useUtilsStore();

function aggregateExpenses<T extends string>(
  expenses: Expense[] | undefined,
  keyGetter: (item: Expense) => T,
  total: number,
  nameMapper?: (key: T) => string
) {
  const aggregated = (expenses || []).reduce((acc: Record<T, number>, item) => {
    const key = keyGetter(item);
    acc[key] = (acc[key] || 0) + Number(item.converted_amount);
    return acc;
  }, {} as Record<T, number>);

  const result: Record<
    T,
    { name: string; value: number; percent: string }
  > = {} as Record<T, { name: string; value: number; percent: string }>;

  for (const [key, value] of Object.entries(aggregated) as [T, number][]) {
    const name = nameMapper ? nameMapper(key) : key;
    result[key] = {
      name,
      value,
      percent: total > 0 ? ((value / total) * 100).toFixed(2) : "0.00",
    };
  }

  return result;
}

const expensesByUser = computed(() => {
  const total = spent.value || 0;
  return aggregateExpenses(expenses.value, item => item.username || "", total);
});

const expensesByCategory = computed(() => {
  const total = spent.value || 0;
  return aggregateExpenses(
    expenses.value,
    item => String(item.category || "Inne"),
    total,
    key => mapCategoryBudget(Number(key)).name
  );
});


const membersItem = computed(
  () => useMembersStore().members.filter((e) => !e.is_guest) || []
);
const {userData} = useAuthStore();
const {isOwner} = userData;
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection
        subtitle="Wydatki"
        button
        button-text="Dodaj"
        :button-action="toggleForm"
      />
    </template>

    <template #content>
      <v-col cols="12" class="text-h5 font-weight-bold">
        <!-- Budget Overview -->
        <v-row class="budget-overview-gap">
          <!-- Budget Card -->
          <AppCard>
            <p class="mb-4">Budżet</p>
            <p class="text-h3 font-weight-bold">
              {{ budget }} {{ budgetCurrency }}
            </p>
          </AppCard>

          <!-- Spent Card -->
          <AppCard>
            <span>Wydano</span>
            <BudgetContent
              :showCurrency="false"
              :content="{
                amount: budget,
                currency: budgetCurrency,
                expenses: spent,
              }"
            />
          </AppCard>

          <!-- Remaining Budget Card -->
          <AppCard>
            <p class="mb-3">{{remaining>=0?"Pozostało":"Debet"}}</p>
            <p
              class="text-h3 font-weight-bold"
              :class="remaining >= 0 ? 'difference-positive' : 'difference-negative'"
            >
              {{ remaining.toFixed(2) }} {{ budgetCurrency }}
            </p>
          </AppCard>

          <!-- Form for adding expenses -->
          <v-col cols="12" v-if="showForm">
            <v-row>
              <ExpenseForm
                :isOwnerTrip = "isOwner(trip?.creator?.id || 0)"
                :members="membersItem"
                @cancelForm="showForm = false"
                @submitted="onExpenseAdded"
                class="form-container"
              />
            </v-row>
          </v-col>

          <!-- List of expenses -->
          <v-col cols="12">
            <v-row>
              <AppCard cols="12">
                <!-- Header with title and filter button -->
                <v-row
                  justify="space-between"
                  align="center"
                  class="mb-4"
                  no-gutters
                >
                  <span>Wydatki</span>
                  <AppButton
                    color="primary"
                    @click="showFilters = true"
                    height-auto
                    font-auto
                    dense
                    text="Filtruj"
                  >
                    <v-icon start>mdi-filter</v-icon>
                  </AppButton>
                </v-row>

                <!-- Expenses List -->
                <ExpensesList
                  :isOwnerTrip = "isOwner(trip?.creator?.id || 0)"
                  variant="manage"
                  :expenses="expenses"
                  :config="appliedFilters"
                />
              </AppCard>
            </v-row>
          </v-col>
          <v-row>
            <v-col cols="12" sm="6">
              <AppCard>
                <span>Wydatki - Kategorie</span>
                <v-row
                  v-for="(user, index) in expensesByCategory"
                  :key="index"
                  class="mb-2"
                >
                  <v-col cols="6" class="text-subtitle-1">
                    {{ user.name }}
                  </v-col>
                  <v-col cols="6" class="text-right text-subtitle-1">
                    {{ user.percent }}%
                  </v-col>
                  <v-col cols="12">
                    <v-progress-linear
                      :model-value="Number(user.percent)"
                      color="success"
                      height="6"
                      rounded
                      bg-color="grey-lighten"
                    />
                  </v-col>
                </v-row>
              </AppCard>
            </v-col>
            <v-col cols="12" sm="6">
              <AppCard>
                <span>Wydatki - Uczestnicy</span>
                <v-row
                  v-for="(user, index) in expensesByUser"
                  :key="index"
                  class="mb-2"
                >
                  <v-col cols="6" class="text-subtitle-1">
                    {{ user.name }}
                  </v-col>
                  <v-col cols="6" class="text-right text-subtitle-1">
                    {{ user.percent }}%
                  </v-col>
                  <v-col cols="12">
                    <v-progress-linear
                      :model-value="Number(user.percent)"
                      color="success"
                      height="6"
                      rounded
                      bg-color="grey-lighten"
                    />
                  </v-col>
                </v-row>
              </AppCard>
            </v-col>
          </v-row>
        </v-row>
      </v-col>

      <v-dialog v-model="showFilters" max-width="500">
        <v-card class="pa-3">
          <v-card-title class="text-h6">Filtry</v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col cols="12">
                <v-select
                  v-model="selectedCategory"
                  :items="budgetCategory"
                  item-title="name"
                  item-value="id"
                  label="Kategoria"
                  variant="outlined"
                  clearable
                />
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="selectedParticipant"
                  :items="members"
                  item-title="name"
                  item-value="userId"
                  label="Uczestnik"
                  :disabled="members.length === 0"
                  variant="outlined"
                  bg-color="transparent"
                  clearable
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-date-input
                  v-model="dateFrom"
                  max-width="auto"
                  variant="outlined"
                  prepend-icon=""
                  prepend-inner-icon="mdi-calendar"
                  color="primary"
                  label="Od"
                  :clearable="true"
                  header-color="primary"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-date-input
                  v-model="dateTo"
                  max-width="auto"
                  variant="outlined"
                  prepend-icon=""
                  prepend-inner-icon="mdi-calendar"
                  color="primary"
                  :clearable="true"
                  header-color="primary"
                  label="Do"
                />
              </v-col>
            </v-row>
            <v-row justify="center">
              <AppButton
                color="accent"
                text="Anuluj"
                @click="showFilters = false"
              />
              <AppButton color="primary" text="Zastosuj" @click="filter" />
            </v-row>
          </v-card-text>
        </v-card>
      </v-dialog>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.difference-positive {
  color: rgba(22, 163, 74, 0.75);
}
.difference-negative
{
  color:rgb(var(--v-theme-delete));
}

</style>
