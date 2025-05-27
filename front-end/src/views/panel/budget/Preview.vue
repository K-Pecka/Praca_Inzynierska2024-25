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
import { computed, ref, watch } from "vue";
import { useMembersStore } from "@/stores/trip/useMembersStore";
import { Expense } from "@/types";
import { VDateInput } from "vuetify/labs/components";
import dayjs from "dayjs";
import { useAuthStore, useUtilsStore } from "@/stores";
const appliedFilters = ref<{
  category: string | null;
  user: string | null;
  date_from: string | null;
  date_to: string | null;
}>({
  category: null,
  user: null,
  date_from: null,
  date_to: null,
});

const toggleForm = () => {
  showForm.value = !showForm.value;
};
const { budget: budgetStore, trip: tripStore } = useTripStore();
const { getTripDetails, updateTripBudget } = tripStore;
const { trip, isLoading_trip } = getTripDetails();

const members = computed(() => {
  if (trip.value !== undefined) {
    useMembersStore().setData(trip.value);
  }
  return useMembersStore().members.filter((e) => !e.is_guest) || [];
});

const { getExpensByTrip } = budgetStore;

const onExpenseAdded = () => {
  showForm.value = false;
};

const {
  expensesByTrip: expenses,
  isLoading_expenses,
  refetch_expenses,
} = getExpensByTrip();

const budget = computed(() => Number(trip.value?.budget_amount) ?? 0);
const budgetCurrency = computed(() => "PLN");
const formatDate = (date?: string | Date | null) =>
  date ? dayjs(date).format("YYYY-MM-DD") : null;
const filter = () => {
  showFilters.value = false;
  budgetStore.setFilters({
    category: appliedFilters.value.category ?? null,
    user: appliedFilters.value.user ?? null,
    date_from: formatDate(appliedFilters.value.date_from),
    date_to: formatDate(appliedFilters.value.date_to),
  });
  refetch_expenses();
};
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

  const result: Record<T, { name: string; value: number; percent: string }> =
    {} as Record<T, { name: string; value: number; percent: string }>;

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
  return aggregateExpenses(
    expenses.value,
    (item) => item.username || "",
    total
  );
});

const expensesByCategory = computed(() => {
  const total = spent.value || 0;
  return aggregateExpenses(
    expenses.value,
    (item) => String(item.category || "Inne"),
    total,
    (key) => mapCategoryBudget(Number(key)).name
  );
});

const { userData } = useAuthStore();
const { isOwner } = userData;
const isEditing = ref(false);
const editableBudget = ref(budget.value);
function toggleEdit() {
  editableBudget.value = budget.value;
  isEditing.value = true;
}
const { getTripId } = useUtilsStore();
function saveBudget() {
  if (editableBudget.value <= 0 || editableBudget.value === budget.value || String(editableBudget.value).length >= 8) {
    return;
  }
  isEditing.value = false;
  updateTripBudget.mutateAsync({
    newBudget: { budget_amount: Number(editableBudget.value) },
    param: { tripId: String(getTripId()) },
  });
}

function cancelEdit() {
  isEditing.value = false;
  editableBudget.value = budget.value;
}
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
            <p class="mb-4 d-flex align-center" style="gap: 8px">
              Budżet
              <v-icon
                v-if="!isEditing && isOwner(trip?.creator?.id || 0)"
                class="edit-icon"
                @click="toggleEdit"
                style="cursor: pointer"
                color="primary"
                size="20"
                >mdi-pencil</v-icon
              >
            </p>
            <template v-if="isLoading_trip">
              <v-row justify="center">
                <v-col cols="auto">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    size="32"
                  />
                </v-col>
              </v-row>
            </template>
            <div v-else-if="!isEditing">
              <p class="text-h3 font-weight-bold mb-0" style="line-height: 1.2">
                {{ budget.toFixed(2) }} {{ budgetCurrency }}
              </p>
            </div>

            <div
              v-else
              class="edit-budget d-flex align-center"
              style="gap: 8px"
            >
              <v-text-field
                v-model.number="editableBudget"
                type="text"
                variant="outlined"
                dense
                style="max-width: 75%"
                class="mb-0"
                :rules="[
                  (v) => !isNaN(Number(v)) && v > 0 || 'Budżet musi być większy niż 0',
                  (v) =>
                    editableBudget != budget ||
                    'Nie można zapisać tej samej wartości',
                  (v) => String(v).length <= 8 || 'Budżet jest zbyt duża',
                ]"
                placeholder="Wprowadź budżet"
              />
              <v-btn
                icon
                color="primary"
                @click="saveBudget"
                title="Zapisz"
                size="36"
                style="margin-bottom: 24px; height: 36px; min-width: 36px"
                rounded
              >
                <v-icon>mdi-check</v-icon>
              </v-btn>
              <v-btn
                icon
                color="accent"
                @click="cancelEdit"
                title="Anuluj"
                size="36"
                style="margin-bottom: 24px; height: 36px; min-width: 36px"
                rounded
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
          </AppCard>

          <!-- Spent Card -->
          <AppCard>
            <span>Wydano</span>
            <template v-if="isLoading_trip">
              <v-row justify="center">
                <v-col cols="auto">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    size="32"
                  />
                </v-col>
              </v-row>
            </template>
            <BudgetContent
              v-else
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
            <template v-if="isLoading_trip">
              <v-row justify="center">
                <v-col cols="auto">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    size="32"
                  />
                </v-col>
              </v-row>
            </template>
            <p
              v-else
              class="text-h3 font-weight-bold"
              :class="
                remaining >= 0 ? 'difference-positive' : 'difference-negative'
              "
            >
              {{ remaining.toFixed(2) }} {{ budgetCurrency }}
            </p>
          </AppCard>

          <!-- Form for adding expenses -->
          <v-col cols="12" v-if="showForm">
            <v-row>
              <ExpenseForm
                :isOwnerTrip="isOwner(trip?.creator?.id || 0)"
                :members="members"
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
                  v-if="!isLoading_expenses"
                  :isOwnerTrip="isOwner(trip?.creator?.id || 0)"
                  variant="manage"
                  :expenses="expenses"
                />
                <template v-else>
                  <v-row justify="center">
                    <v-col cols="auto">
                      <v-progress-circular
                        indeterminate
                        color="primary"
                        size="64"
                      />
                    </v-col>
                  </v-row>
                </template>
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
                  v-model="appliedFilters.category"
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
                  v-model="appliedFilters.user"
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
                  v-model="appliedFilters.date_from"
                  :min="trip?.start_date"
                  :max="appliedFilters.date_to ?? trip?.end_date"
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
                  v-model="appliedFilters.date_to"
                  :min="appliedFilters.date_from ?? trip?.start_date"
                  :max="trip?.end_date"
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
.difference-negative {
  color: rgb(var(--v-theme-delete));
}
</style>
