<script setup lang="ts">
import {Expense} from "@/types";
import AppCard from "@/components/AppCard.vue";
import {useUtilsStore} from "@/stores";

const {mapCategoryBudget} = useUtilsStore();
const {expense} = defineProps<{
  expense: Expense;
  variant?: "manage" | "view";
  noIcon?: boolean;
}>();
const {icon, name: categoryName} = mapCategoryBudget(expense.category);
const currencyValue =
    expense.currency != "PLN" ? `(${expense.converted_amount} PLN)` : "";
</script>

<template>
  <AppCard
      class="background-card"
      no-padding
      bg-transparent
      :elevation="0"
      cols="12"
  >
    <v-card-text class="text-h6 font-weight-bold">
      <v-row justify="space-between" align="center">

        <!-- Expense Icon and Title -->
        <v-col cols="auto">
          <v-row align="center">
            <v-sheet class="rounded-xl bg-red mr-4">
              <v-icon size="24" class="ma-1">
                {{ icon }}
              </v-icon>
            </v-sheet>
            <v-row class="flex-column" justify="center" no-gutters>
              <span>{{ expense.title }}</span>
              <span class="text-subtitle-1 font-weight-medium">
                <span> {{ expense.date }} </span>
                <span class="px-3"> {{ expense.username }}</span>
                <span class="notes"> {{ expense?.note ?? "" }}</span>
                <span class="category">{{ categoryName }}</span>
              </span>
            </v-row>
          </v-row>
        </v-col>

        <!-- Expense Amount -->
        <v-col class="text-h5" cols="auto">
          <v-row class="justify-space-between" no-gutters>
            <v-row class="flex-column justify-center">
              <strong class="text-black-70 mr-2">
                {{ expense.amount }} {{ expense.currency }}
              </strong>
              <span v-if="currencyValue" class="text-subtitle-1 text-grey-darken-1"
                    style="line-height: 0.8">
                {{ currencyValue }}
              </span>
              <span v-else class="text-subtitle-1" style="line-height: 0.8">
                ({{ expense.amount }} {{ expense.currency }})
              </span>
            </v-row>

            <v-btn variant="flat" class="bg-transparent px-0" v-if="!noIcon">
              <v-icon
                  v-if="!!variant && variant === 'manage'"
                  size="28"
                  class="amount"
              >
                mdi-trash-can-outline
              </v-icon>
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </AppCard>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.category {
  color: rgb($primary-color);
  font-weight: 400;
}

.notes {
  color: #757575;
}

.amount {
  color: #e74c3c;
}

.background-card {
  background-color: rgb(var(--v-theme-background));
}
</style>
