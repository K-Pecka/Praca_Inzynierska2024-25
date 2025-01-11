<template>
  <Section>
    <template #title>
      <h1>Logowanie</h1>
    </template>
    <template #content>
      <form @submit.prevent="handleSubmit">
      <div v-for="(inputsData, index) in inputs" :key="index" class="input-container">
        <InputWithLabel 
          :inputData="inputsData" 
          v-model="formValues[inputsData.name]" 
        />    
      </div>
      <button type="submit">Zapisz</button>
    </form>
    </template>
  </Section>
    
  </template>
  
  <script lang="ts" setup>
  import { ref } from 'vue';
  import InputWithLabel from '@/components/InputWithLabel.vue';
  import Section from "@/components/Section.vue";

  const inputs = ref([
    {
      name: 'email',
      label: 'Podaj Email:',
      type: 'email',
      placeholder: 'Wprowadź email',
    },
    {
      name: 'password',
      label: 'Podaj Hasło:',
      type: 'password',
      placeholder: 'Wprowadź hasło',
    },
  ]);
  
  const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map((input) => [input.name, '']))
  );
 
  const handleSubmit = () => {
    console.log('Wartości formularza:', formValues.value);
  };
  </script>
  
  <style scoped>
  .input-container {
    margin-bottom: 1rem;
  }
  </style>
  