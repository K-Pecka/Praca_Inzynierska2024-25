<script setup lang="ts">
import DebtItem from "./DebtItem.vue";
import { DebtDetails } from "@/types";

const { debts } = defineProps<{
  debts?: DebtDetails[];
  variant?: "manage" | "view";
  config?: Record<string, any>;
  limit?: number;
  noIcon?: boolean;
  isOwnerTrip?: boolean;
}>();
</script>


<template>
  <div class="expense-list w-100 ga-6">
    <template v-for="(debt, index) in debts" :key="index">
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
