<script setup lang="ts">
import { Expense } from "@/type";
import ExpenseItem from "./ExpenseItem.vue";
defineProps<{expenses: Expense[]}>();
</script>
<template>
  <div class="participant-list">
    <ExpenseItem v-for="expense in expenses" :key="expense.note" :expense="expense" />
  </div>
</template>

<style scoped lang="scss">
.participant-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
