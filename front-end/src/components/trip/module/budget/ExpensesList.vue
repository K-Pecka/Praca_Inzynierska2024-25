<script setup lang="ts">
import { computed } from "vue";
import dayjs from "dayjs";
import isSameOrBefore from "dayjs/plugin/isSameOrBefore";
import ExpenseItem from "./ExpenseItem.vue";
import { Expense } from "@/types";

dayjs.extend(isSameOrBefore);

const { expenses, variant, config, limit, noIcon } = defineProps<{
  expenses?: Expense[];
  variant?: "manage" | "view";
  config?: Record<string, any>;
  limit?: number;
  noIcon?: boolean;
}>();

const visibleExpenses = computed(() => {
  if (!expenses) return [];

  let filtered = [...expenses].sort(
    (a, b) => dayjs(b.date).valueOf() - dayjs(a.date).valueOf()
  );

  if (config?.category) {
    filtered = filtered.filter((e) => e.category === config.category);
  }

  if (config?.participants) {
    filtered = filtered.filter((e) => e.user === config.participants);
  }

  if (config?.dateFrom) {
    filtered = filtered.filter((e) =>
      dayjs(e.date).isSame(dayjs(config.dateFrom)) ||
      dayjs(e.date).isAfter(dayjs(config.dateFrom))
    );
  }

  if (config?.dateTo) {
    filtered = filtered.filter((e) =>
      dayjs(e.date).isSame(dayjs(config.dateTo)) ||
      dayjs(e.date).isBefore(dayjs(config.dateTo))
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
      :no-icon="noIcon"
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
