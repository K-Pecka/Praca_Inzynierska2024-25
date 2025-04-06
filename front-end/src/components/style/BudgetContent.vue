<script lang="ts" setup>
import { defineProps } from "vue";
import { BudgetData } from "@/type/interface";

const props = defineProps<{ content: BudgetData }>();

const safeDivision = (numerator: number, denominator: number, percent: boolean) => {
  if (denominator === 0) {
    return percent ? 100 : 0;
  }
  return (numerator / denominator).toFixed(2);
};
</script>

<template>
  <div v-if="typeof props.content === 'object' && props.content !== null">
    <div class="amount my-2">
      <span class="text-h5 font-weight-bold">
        {{ props.content.amount }} {{ props.content.currency }}
      </span>
    </div>

    <v-progress-linear
      :model-value="safeDivision(props.content.expenses, props.content.convertedAmount, true)"
      height="6"
      rounded
      color="green"
      background-color="grey-lighten-3"
    ></v-progress-linear>

    <v-row justify="space-between" class="mt-1">
      <span class="text-green font-weight-medium">
        {{ props.content.convertedAmount }} {{ props.content.convertedCurrency }}
      </span>
      <span class="text-grey-darken-1">
        {{ safeDivision(props.content.expenses, props.content.convertedAmount, false) }}%
      </span>
    </v-row>
  </div>
</template>
<style scoped lang="scss">
/* ! */
</style>