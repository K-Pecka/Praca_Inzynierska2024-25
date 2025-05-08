<script setup lang="ts">
import ExpenseItem from "./ExpenseItem.vue";
import { computed } from "vue";
import { Expense } from "@/types";
const { expenses, variant, config, limit } = defineProps<{
  expenses?: Expense[];
  variant?: "manage" | "view";
  config?: Record<string, any>;
  limit?: number;
}>();

function convertToDate(dateStr: string): number {
  return new Date(dateStr).getTime();
}

const visibleExpenses = computed(() => {
  if (!expenses) return [];

  let filtered = [...expenses].sort((b, a) =>
    convertToDate(a.date) - convertToDate(b.date)
  );

  if (config?.category) {
    filtered = filtered.filter((e) => e.category === config.category);
  }
  if (config?.participants) {
    filtered = filtered.filter((e) => e.user === config.participants);
  }
  if (config?.dateFrom) {
    filtered = filtered.filter(
      (e) => convertToDate(e.date) >= convertToDate(config.dateFrom)
    );
  }
  if (config?.dateTo) {
    filtered = filtered.filter(
      (e) => convertToDate(e.date) <= convertToDate(config.dateTo)
    );
  }

  return limit ? filtered.slice(0, limit) : filtered;
});
</script>

<template>
  <div class="expense-list w-100 ga-6">
    <ExpenseItem
      v-for="(expense, index) in visibleExpenses"
      :key="index"
      :expense="expense"
      :variant="variant"
    />
  </div>
</template>

<style scoped>
.expense-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
