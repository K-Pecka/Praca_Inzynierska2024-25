<script setup lang="ts">
import { Expense} from "@/type";
defineProps<{
    expense?: Expense;
}>();
</script>
<template>
    <div class="participant-item">
      <div class="participant-left">
        <v-icon size="48">mdi-food-fork-drink</v-icon>
  
        <div class="participant-texts">
          <strong class="participant-name">{{ expense?.title }}</strong>
          <div class="email-row">
            <span class="participant-email">{{ expense?.date }} {{ expense?.type }} {{ expense?.note }}</span>
          </div>
        </div>
      </div>
  
      <div class="price">
        <span size="24">{{expense?.amount}} {{expense?.currency}}</span>
      </div>
    </div>
  </template>
  
  <style scoped lang="scss">
  .participant-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  
    background-color: rgb(var(--v-theme-background));
    border-radius: 12px;
    padding: 1rem 1.5rem;
  
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
  
  .participant-left {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .participant-texts {
    display: flex;
    flex-direction: column;
  }
  
  .participant-name {
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.25rem;
  }
  
  .email-row {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  
  .participant-email {
    font-size: 0.9rem;
    color: #555;
  }
  
  .price {
    background: transparent;
    border: none;
    cursor: pointer;
    color: #e44a3e;
    display: flex;
    align-items: center;
    transition: opacity 0.2s ease;
  
    &:hover {
      opacity: 0.8;
    }
  }
  </style>
  