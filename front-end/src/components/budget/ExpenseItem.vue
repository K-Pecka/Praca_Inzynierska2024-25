<script setup lang="ts">
import { Expense } from "@/types";
import AppCard from "./AppCard.vue";
import { useUtilStore } from "@/stores";
const { mapCategoryBudget} = useUtilStore();
const props=defineProps<{
  expense: Expense;
  variant?: "manage" | "view";
}>();
const {icon, name:categoryName} = mapCategoryBudget(props.expense.category);
</script>

<template>
  <AppCard class="expense-item backgroud-card">
    <div class="d-flex align-center">
      <v-icon size="32" class="mr-4">{{icon}}</v-icon>
      <div class="info">
        <h4>{{ expense.title }}</h4>
        <p>
          {{ expense.date }} - <span class="category">{{categoryName}}</span>
          <span class="notes"> - {{ }}</span>
        </p>
      </div>
    </div>
    <template v-if="!!variant && variant === 'manage'">
      <div class="amount">
      <strong>{{ expense.amount }}{{ expense.currency }}</strong>
      <v-icon :style="{ marginTop: '-6px' }">mdi-trash-can-outline</v-icon>
    </div>
      </template> 
    <div v-else>
      <strong>{{ expense.amount }} {{ expense.currency }}</strong>
    </div>
  </AppCard>
</template>

<style scoped>
.expense-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  color: #4a90e2;
  font-weight: bold;
}

.notes {
  color: #757575;
}

.amount {
  font-size: 16px;
  color: #e74c3c;
}
</style>
