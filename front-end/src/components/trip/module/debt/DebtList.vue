<script setup lang="ts">
import DebtItem from "./DebtItem.vue";
import { DebtDetails } from "@/types";

const { debts,limit } = defineProps<{
  debts?: DebtDetails[];
  limit?: number;
}>();

</script>


<template>
  <div class="expense-list w-100 ga-6">
    <template v-for="(debt, index) in debts?.slice(0,limit)" :key="index">
      <DebtItem
        v-if="debt?.members.length > 0"
        :debt="debt"
      />
    </template>
  </div>
</template>

<style scoped>
.expense-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
