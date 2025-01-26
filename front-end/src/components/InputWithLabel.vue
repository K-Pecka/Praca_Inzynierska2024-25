<template>
  <div class="input-wrapper">
    <label :for="inputData.name" class="input-label" :class="{ required: inputData.config?.required }">{{ inputData.label }}</label>

    <input
      :name="inputData.name"
      :id="inputData.name"
      :type="inputData.type"
      :placeholder="inputData.placeholder"
      :value="modelValue"
      @input="handleInput"
      class="input"
      :class="{ error: inputData.error && inputData.error.length > 0 }"
    />
    <div>
      <span v-for="(error, index) in inputData.error" :key="index" class="showError">{{ error }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue';

interface InputData {
  name: string;
  label: string;
  type?: string;
  placeholder: string;
  config?: Config;
  error?: string[];
}
interface Config{
  required: Boolean
}

const emit = defineEmits(['update']);
const props = defineProps({
  inputData: {
    type: Object as () => InputData,
    required: true
  },
  config:{
    type: Object as () => Config
  },
  modelValue: {
    type: String,
    required: true
  }
});

const handleInput = (event: Event) => {
  const name = (event.target as HTMLInputElement).name;
  const value = (event.target as HTMLInputElement).value;
  
  emit('update', name, value);
};
</script>

<style scoped lang="scss">
@use "@/assets/style" as *;
.error{
  border: 1px solid red;
}
.required::after{
  content: " *";
  color:red;
}
.input-wrapper {
  display: flex;
  flex-direction: column;
  margin: 1.5rem auto;
}
.input-label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}
.input {
  padding: 0.5rem;
  font-size: 1rem;
}

span {
  position: relative;
}
.showError {
  font-size:0.7rem;
  display: block;
}
</style>
