<script lang="ts" setup>
import {BudgetData} from "@/types/interface";
import {useUtilsStore} from "@/stores";

const {content, showCurrency} = defineProps<{ content: BudgetData; showCurrency?: boolean }>();
const {safeDivision} = useUtilsStore();
</script>

<template>
  <v-col v-if="typeof content === 'object' && content !== null">
    <v-row class="flex-column">
      <span class="text-h4 color-text font-weight-bold" v-if="showCurrency === true">
        {{ content.amount }} {{ content.currency }}
      </span>

      <v-progress-linear
          :model-value="safeDivision(content.expenses, content.amount, true)"
          height="6"
          rounded
          class="expenses-green my-5"
          background-color="grey-lighten-3"
      ></v-progress-linear>

      <v-row justify="space-between" class="px-3">
        <span class="text-h6 expenses-green" style="font-weight: bold;">
          {{ content.expenses.toFixed(2) }} {{ content.currency }}
        </span>
        <span class="text-grey-darken-1 text-h6" style="font-weight: bold">
          {{ safeDivision(content.expenses, content.amount, true) }}%
        </span>
      </v-row>
    </v-row>


  </v-col>
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