<script setup lang="ts">
import ExpenseItem from "../expense/ExpenseItem.vue";
import { Expense } from "@/types/";

const { expenses, variant, config, limit, noIcon,isOwnerTrip } = defineProps<{
  expenses?: Expense[];
  variant?: "manage" | "view";
  config?: Record<string, any>;
  limit?: number;
  noIcon?: boolean;
  isOwnerTrip?: boolean;
}>();

</script>


<template>
  <div class="expense-list w-100 ga-6">
    <ExpenseItem
      v-for="(expense, index) in expenses"
      :key="index"
      :isOwnerTrip=isOwnerTrip
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
