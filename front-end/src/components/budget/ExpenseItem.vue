<script setup lang="ts">
import AppCard from "./AppCard.vue";
import { defineProps } from "vue";

defineProps<{
  title: string;
  category: string;
  date: string;
  amount: number;
  notes: string;
}>();
</script>

<template>
  <AppCard class="expense-item">
    <div class="d-flex align-center">
      <v-icon size="32">mdi-food-fork-drink</v-icon>
    <div class="info">
      <h4>{{ title }}</h4>
      <p>
        {{ date }} - <span class="category">{{ category }}</span> 
        <span class="notes"> - {{ notes }}</span>
      </p>
    </div>
    </div>
    
    <div class="amount">
      <strong>{{ amount }} EUR</strong>
      <v-icon>mdi-trash-can-outline</v-icon>
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
