<script lang="ts" setup>
import { defineProps } from "vue";
import { BudgetData } from "@/types/interface";

const props = defineProps<{ content: BudgetData;showCurrency?:boolean }>();

const safeDivision = (numerator: number, denominator: number, percent: boolean) => {
  if (denominator === 0) {
    return percent ? 100 : 0;
  }
  if(percent) {
    return ((numerator / denominator) * 100).toFixed(2);
  }
  return (numerator / denominator).toFixed(2);
};
console.log("BudgetContent", typeof props.showCurrency);
</script>

<template>
  <div v-if="typeof props.content === 'object' && props.content !== null">
    <div>
      <span class="text-h5 font-weight-bold" v-if="props.showCurrency === true">
        {{ props.content.expenses }} {{ props.content.currency }}
      </span>
    </div>

    <v-progress-linear
      :model-value="safeDivision(props.content.expenses, props.content.amount, true)"
      height="6"
      rounded
      class="expenses-green my-5"
      background-color="grey-lighten-3"
    ></v-progress-linear>

    <v-row justify="space-between" class="px-3">
      <span class="text-h6 expenses-green" style="font-weight: bold;">
        {{ props.content.convertedAmount.toFixed(2) }} {{ props.content.convertedCurrency }}
      </span>
      <span class="text-grey-darken-1 text-h6" style="font-weight: bold">
        {{ safeDivision(props.content.expenses, props.content.amount, true) }}%
      </span>
    </v-row>
  </div>
</template>
<style scoped lang="scss">
  .expenses-green {
    color: rgba(22, 163, 74, .75)
  }
  .progress {
  height: 100%;
  background-color: rgba(22, 163, 74, .75);
  transition: width 0.3s ease-in-out;
}
.progress.overflow {
  background-color: #f44336;
  transition: width 0.3s ease-in-out;
}
</style>