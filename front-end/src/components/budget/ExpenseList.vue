<script setup lang="ts">
import ExpenseItem from "./ExpenseItem.vue";

defineProps<{ expenses: Array<{ id: number; title: string; category: string; date: string; amount: number; notes: string }> }>();
</script>

<template>
  <div class="expense-list">
    <ExpenseItem v-for="expense in expenses" :key="expense.id" v-bind="expense" />
  </div>
</template>

<style scoped>
.expense-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
