<script setup lang="ts">
import AppCard from "@/components/budget/AppCard.vue";
import AppButton from "@/components/budget/AppButton.vue";
import AppProgress from "@/components/budget/AppProgress.vue";
import ExpenseList from "@/components/budget/ExpenseList.vue";
import Section from "../../../components/common/Section.vue";
import HeaderSection from "@/components/common/HeaderSection.vue";
import ExpenseForm from "@/components/trip/module/expnese/ExpenseForm.vue";
import BudgetContent from "@/components/ui/BudgetContent.vue";
import { fetchUserById } from "@/api";
import { useUtilsStore } from "@/stores";
import { useTripStore } from "@/stores/trip/useTripStore";
import { useRoute } from "vue-router";
import { budget as budgetCategory } from "@/data/category/budget";
import { computed, ref, watchEffect } from "vue";

const route = useRoute();
const id = route.params.tripId as string;

const { getTripDetails, getExpensesQuery } = useTripStore();
const { mapCategoryBudget } = useUtilsStore();

const { data: tripRaw } = getTripDetails(Number(id));
const { data: expenses } = getExpensesQuery(Number(id));

const budget = computed(() => Number(tripRaw.value?.budget?.amount) ?? 0);
const budgetCurrency = computed(() => tripRaw.value?.budget?.currency ?? "PLN");

const getUserById = async (id: number) => {
  const user = await fetchUserById(id);
  return {
    name: `${user.first_name} ${user.last_name}`,
    userId: id,
  };
};

const members = ref<{ name: string; userId: number }[]>([]);

watchEffect(async () => {
  const membersRaw = tripRaw.value?.members ?? [];
  const pendingRaw = tripRaw.value?.pending_members ?? [];

  const confirmed = await Promise.all(
    membersRaw.map(async (entry) => {
      const id = entry;
      const user = await getUserById(id);
      return { ...user, is_guest: false };
    })
  );

  const pending = await Promise.all(
    pendingRaw.map(async (entry) => {
      const id = typeof entry === 'object' && entry !== null ? entry.id : entry;
      const user = await getUserById(id);
      return { ...user, is_guest: true };
    })
  );

  const userMap = new Map<number, typeof confirmed[0]>();
  for (const user of [...pending, ...confirmed]) {
    userMap.set(user.userId, user);
  }

  members.value = Array.from(userMap.values());
});

const spent = computed(() => {
  return (
    expenses.value?.reduce((acc, expense) => Number(acc) + Number(expense.amount), 0) ?? 0
  );
});

const remaining = computed(() => Number(budget.value) - spent.value);

const categories = computed(() => {
  return [
    ...new Set(expenses.value?.map((expense) => expense.category) ?? []),
  ].map((categoryId) => {
    const category = mapCategoryBudget(categoryId);
    return {
      title: category.name,
      value: categoryId,
      icon: category.icon,
    };
  });
});

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
    dateFrom: dateFrom.value,
    dateTo: dateTo.value,
  };
  showFilters.value = false;
};
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
      <v-container fluid>
        <v-row>
          <v-col cols="12" md="4">
            <AppCard class="summary-card ml-md-0">
              <h3>Budżet</h3>
              <p class="amount">{{ budget }} {{ budgetCurrency }}</p>
            </AppCard>
          </v-col>
          <v-col cols="12" md="4">
            <AppCard class="summary-card">
              <h3>Wydano</h3>
              <BudgetContent
                :showCurrency="false"
                :content="{
                  amount: budget,
                  currency: budgetCurrency,
                  convertedAmount: budget / 4.6,
                  convertedCurrency: 'EUR',
                  expenses: spent,
                }"
              />
            </AppCard>
          </v-col>
          <v-col cols="12" md="4">
            <AppCard class="summary-card mr-md-0">
              <h3>Pozostało</h3>
              <p :class="remaining > 0 ? 'remaining' : 'amount'" :style="remaining <= 0 ? 'color:red' : ''">
                {{ remaining <= 0 ? 0 : remaining }} {{ budgetCurrency }}
              </p>
            </AppCard>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <ExpenseForm v-if="showForm" @cancelForm="showForm = false" class="form-container" />
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <AppCard class="expenses">
              <v-container class="title-container">
                <span class="mb-2">Wydatki</span>
                <AppButton
                  variant="primary"
                  @click="showFilters = true"
                  height-auto
                  font-auto
                  dense
                  text="Filtruj"
                >
                  <v-icon start>mdi-filter</v-icon>
                </AppButton>
              </v-container>

              <ExpenseList
                variant="manage"
                :expenses="expenses"
                :config="appliedFilters"
              />
            </AppCard>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <AppCard class="chart-card ml-0">
              <span class="section-title">Wydatki - Kategorie</span>
            </AppCard>
          </v-col>
          <v-col>
            <AppCard class="chart-card mr-0">
              <span class="section-title">Wydatki - Uczestnicy</span>
            </AppCard>
          </v-col>
        </v-row>
      </v-container>

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
                    bg-color="background"
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
                    bg-color="background"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="dateFrom"
                    label="Data od"
                    type="date"
                    variant="outlined"
                    bg-color="background"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="dateTo"
                    label="Data do"
                    type="date"
                    variant="outlined"
                    bg-color="background"
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
.title-container {
  display: flex;
  justify-content: space-between;
}
.remaining {
  color: #2e7d32;
}
.amount {
  font-size: 1.125rem;
  font-weight: bold;
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
</style>
