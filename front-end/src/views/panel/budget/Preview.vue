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
const { members: membersStore } = useMembersStore();
const members = computed(() => membersStore);
const { budget: budgetStore, trip: tripStore } = useTripStore();
const { getExpensByTrip } = budgetStore;

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
    dateFrom: dateFrom.value==null ? dayjs().format('DD.MM.YYYY') : dayjs((dateFrom.value)).format('DD.MM.YYYY'),
    dateTo: dateTo.value==null ? dayjs().format('DD.MM.YYYY') : dayjs((dateTo.value)).format('DD.MM.YYYY'),
  };
  console.table([dateFrom.value, dateTo.value])
  console.log(appliedFilters);
  showFilters.value = false;
};
const ExpensesByUser = computed(() => {
  return (
    expenses?.value?.reduce((acc: Record<string, number>, item: Expense) => {
      acc[item?.username || ""] =
        (acc[item?.username || ""] || 0) + Number(item.amount);
      return acc;
    }, {} as Record<string, number>) || {}
  );
});
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
            <p class="mb-3">Pozostało</p>
            <p
              class="text-h3 font-weight-bold"
              :class="remaining > 0 ? 'remaining' : 'amount'"
              :style="remaining <= 0 ? 'color:red' : ''"
            >
              {{ remaining <= 0 ? 0 : remaining }} {{ budgetCurrency }}
            </p>
          </AppCard>

          <!-- Form for adding expenses -->
          <v-col cols="12" v-if="showForm">
            <v-row>
              <ExpenseForm
                :members="members"
                @cancelForm="showForm = false"
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
                  variant="manage"
                  :expenses="expenses"
                  :config="appliedFilters"
                />
              </AppCard>
            </v-row>
          </v-col>

          <AppCard cols="6">
            <span>Wydatki - Kategorie</span>
          </AppCard>
          <AppCard cols="6">
            <v-row no-gutters class="d-flex flex-column">
              <span>Wydatki - Uczestnicy</span>
              <v-col
                v-if="ExpensesByUser"
                v-for="(amount, username) in ExpensesByUser"
              >
                <p>
                  <span>
                    {{ username }}
                  </span>
                  <span>
                    {{ amount }}
                  </span>
                </p>
              </v-col>
            </v-row>
          </AppCard>
        </v-row>
      </v-col>

      <v-dialog v-model="showFilters" max-width="500">
        <v-card class="pa-3">
          <v-card-title class="text-h6">Filtry</v-card-title>
          <v-card-text>
            <v-container>
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
            </v-container>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn text @click="showFilters = false">Anuluj</v-btn>
            <v-btn color="primary" @click="filter">Zastosuj</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.remaining {
  color: rgba(22, 163, 74, 0.75);
}
</style>
