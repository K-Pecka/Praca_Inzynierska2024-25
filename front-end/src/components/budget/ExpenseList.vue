<script setup lang="ts">
import ExpenseItem from "./ExpenseItem.vue";

import { useTripStore } from "@/stores/trip/useTripStore";
import { useUtilStore } from "@/stores";
const {getTripId} = useUtilStore();
const {data:expenses,isLoading} = useTripStore().getExpensesQuery(getTripId() as unknown as number);
const { variant, limit } = defineProps<{
  variant?: "manage" | "view";
  limit?: number;
}>();
import { computed} from "vue";
const visibleExpenses = computed(() => {
  if (!expenses.value) return [];
  return limit ? expenses.value.slice(0, limit) : expenses.value;
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
