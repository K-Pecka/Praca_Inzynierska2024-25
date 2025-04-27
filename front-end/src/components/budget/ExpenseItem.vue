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
      <v-icon size="48" class="mr-4">{{icon}}</v-icon>
      <div class="info">
        <h4>{{ expense.title }}</h4>
        <p>
          {{ expense.date }} <span class="category font-regular">{{categoryName}}</span>
          <span class="notes"> {{ expense?.note ?? '' }}</span>
        </p>
      </div>
    </div>
    <template v-if="!!variant && variant === 'manage'">
      <div class="amount">
      <strong class="text-black-70">{{ expense.amount }}{{ expense.currency }}</strong>
      <v-icon :style="{ marginTop: '-6px' }">mdi-trash-can-outline</v-icon>
    </div>
      </template> 
    <div v-else>
      <strong class="text-black-70">{{ expense.amount }} {{ expense.currency }}</strong>
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
  color: rgba(var(--v-theme-primary));
  font-weight: 400;
}

.notes {
  color: #757575;
}

.amount {
  font-size: 16px;
  color: #e74c3c;
}
</style>
