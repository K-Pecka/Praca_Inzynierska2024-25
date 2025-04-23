<script setup lang="ts">
import { Expense} from "@/types";
defineProps<{
    expense?: Expense;
}>();
</script>
<template>
    <div class="participant-item">
      <div class="participant-left">
        <v-img
          src="/picture/expense-item-image.svg"
          width="45"
          height="45"
          class="rounded-circle"/>
  
        <div class="participant-texts">
          <strong class="participant-name text-h6 font-weight-bold">{{ expense?.title }}</strong>
          <div class="email-row">
            <span>{{ expense?.date }} <span class="expense-item-type">{{ expense?.type }}</span> {{ expense?.note }}</span>
          </div>
        </div>
      </div>
  
      <div class="price">
        <span class="expense-item-amount text-subtitle-1">{{expense?.amount}} {{expense?.currency}}</span>
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

  .expense-item-type {
    color: rgb(var(--v-theme-primary), 0.75);
  }

  .expense-item-amount {
    font-weight: bold;
    color: rgb(var(--v-theme-text), 0.75);
    font-family: var(--v-fontFamily);
  }
  
  .participant-texts {
    display: flex;
    flex-direction: column;
  }
  
  .participant-name {
    color: rgb(var(--v-theme-text), 0.75);
    line-height: 1.2;
  }
  
  .email-row {
    display: flex;
    align-items: center;
    gap: 0.25rem;
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
  