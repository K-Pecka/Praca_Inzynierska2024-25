<script setup>
import { ref, computed } from 'vue';
import { useRoute } from "vue-router";
import { useTripStore } from "@/stores/tripStore";

const { getTripDetails } = useTripStore();
const route = useRoute();
const id = Number(route.params.tripId);

const { data: trip, isLoading, error } = getTripDetails(id);

const budget = computed(() => (trip.value?.budget ?? 0));
const expenses = ref([
  { id: 1, category: 'Obiad w restauracji', amount: -17.97, currency: 'PLN', date: '17.12.2024' },
  { id: 2, category: 'Obiad w restauracji', amount: -7.97, currency: 'PLN', date: '17.12.2024' },
  { id: 3, category: 'Obiad w restauracji', amount: -222.97, currency: 'PLN', date: '17.12.2024' },
  { id: 4, category: 'Obiad w restauracji', amount: -17.97, currency: 'PLN', date: '17.12.2024' }
]);

const spent = computed(() => Math.abs(expenses.value.reduce((acc, exp) => acc + exp.amount, 0)));
const progress = computed(() => (spent.value / budget.value) * 100);
</script>

<template>
  <template v-if="isLoading">
    <p>Loadding...</p>
  </template>
  <v-container v-else>
    <v-row justify="center">
      <v-col cols="12" md="6" lg="4" class="text-center">
        <v-progress-circular
          :model-value="progress"
          :size="250"
          :width="20"
          color="#8EFF84"
        >
          <div class="progress-text">
            {{ spent.toFixed(2) }}/{{ Number(budget) }} PLN
          </div>
        </v-progress-circular>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <h3 class="text-center mt-5">Wydatki</h3>

        <v-list class="expenses-list">
          <v-list-item v-for="expense in expenses" :key="expense.id">
            <v-card class="expense-card d-flex align-center">

              <div class="d-flex align-center flex-grow-1">
                <v-icon class="mr-3" color="primary">mdi-food</v-icon>
                <span class="expense-category">{{ expense.category }}</span>
              </div>

              <div class="expense-details d-flex justify-end">
                <span class="expense-amount">{{ expense.amount }} {{ expense.currency }}</span>
                <span class="expense-date">{{ expense.date }}</span>
              </div>
            </v-card>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.v-container {
  max-width: 1000px;
  margin: auto;
}

.progress-text {
  font-size: 1.2rem;
  font-weight: bold;
  color: rgb(var(--v-theme-text));
}

.expenses-list {
  margin-top: 10px;
  width: 100%;
  background-color: transparent;
}

.expense-card {
  padding: 1rem;
  border-radius: 1rem;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #000000;
  box-shadow: 0px 3px 7px rgba(0, 0, 0, 0.1);
}

.expense-category {
  font-size: 1rem;
  font-weight: bold;
}

.expense-details {
  min-width: 200px;
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.expense-amount {
  font-weight: bold;
  color: #d32f2f;
  text-align: right;
}

.expense-date {
  color: #666;
  text-align: right;
}
</style>
