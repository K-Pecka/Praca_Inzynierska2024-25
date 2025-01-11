<template>
    <div class="input-wrapper">
      <!-- Etykieta -->
      <label :for="inputData.name" class="input-label">{{ inputData.label }}</label>
      <!-- Pole input -->
      <input
        :id="inputData.name"
        :type="inputData.type"
        :placeholder="inputData.placeholder"
        :value="modelValue"
        @input="updateValue"
        class="input"
      />
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps, defineEmits } from 'vue';
  
  // Dane wejściowe
  defineProps({
    inputData: {
      type: Object as () => {
        name: string;
        label: string;
        type: string;
        placeholder: string;
      },
      required: true,
    },
    modelValue: {
      type: String,
      required: true,
    },
  });
  
  // Emitowanie zdarzeń dla `v-model`
  const emit = defineEmits(['update:modelValue']);
  
  // Aktualizacja wartości
  const updateValue = (event: Event) => {
    emit('update:modelValue', (event.target as HTMLInputElement).value);
  };
  </script>
  
  <style scoped>
  .input-wrapper {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }
  .input-label {
    margin-bottom: 0.5rem;
    font-weight: bold;
  }
  .input {
    padding: 0.5rem;
    font-size: 1rem;
  }
  </style>
  