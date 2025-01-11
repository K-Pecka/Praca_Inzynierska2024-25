<template>
    <div class="input-wrapper">
      
      <label :for="inputData.name" class="input-label">{{ inputData.label }}</label>
      
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

  defineProps({
    inputData: {
      type: Object as () => {
        name: string;
        label: string;
        type?: string;
        placeholder: string;
      },
      required: true,
    },
    modelValue: {
      type: String,
      required: true,
    },
  });
  
  const emit = defineEmits(['update:modelValue']);

  const updateValue = (event: Event) => {
    emit('update:modelValue', (event.target as HTMLInputElement).value);
  };
  </script>
  
  <style scoped>
  .input-wrapper {
    display: flex;
    flex-direction: column;
    margin:1.5rem auto;
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
  