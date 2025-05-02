<script setup lang="ts">
import ExpenseItem from "./ExpenseItem.vue";

import { useTripStore } from "@/stores/trip/useTripStore";
import { useUtilsStore } from "@/stores";
const {getTripId} = useUtilsStore();
const {data:expenses,isLoading} = useTripStore().getExpensesQuery(getTripId() as unknown as number);
const { variant, limit,config } = defineProps<{
  variant?: "manage" | "view";
  config?: Record<string, any>;
  limit?: number;
}>();
import { computed, ref} from "vue";
function convertToDate(dateStr : string): number {
  const [day, month, year] = dateStr.split('.');
  return new Date(`${year}-${month}-${day}`).getTime();
}
const visibleExpenses = computed(() => {
  if (!expenses.value) return [];
  const expense = ref([...expenses.value]);
  expense.value = expense.value.sort((b, a) => 
    convertToDate(a.date) - convertToDate(b.date)
  );
  if (config?.category) {
    expense.value = expense.value.filter((expense) => expense.category === config.category);
  }
  if (config?.user) {
    expense.value = expense.value.filter((expense) => expense.user === config.user);
  }
  if (config?.dateFrom) {
    expense.value = expense.value.filter((expense) => convertToDate(expense.date) >= convertToDate(config.dateFrom));
  }
  if (config?.dateTo) {
    expense.value = expense.value.filter((expense) => convertToDate(expense.date) <= convertToDate(config.dateTo));
  }
  console.log("expense", expense.value);
  return limit ? expense.value.slice(0, limit) : expense.value;
});
</script>

<template>
  <div class="expense-list w-100">
    <ExpenseItem
      v-for="(expense, index) in visibleExpenses"
      :key="index"
      :expense="expense"
      :variant="variant"
      v-if="!isLoading"
    >
    </ExpenseItem>
    <div v-else>
      Ładowanie...
    </div>
  </div>
</template>

<style scoped>
.expense-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
