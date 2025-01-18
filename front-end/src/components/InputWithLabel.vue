<template>
  <div class="input-wrapper">
    <label :for="inputData.name" class="input-label">{{ inputData.label }}</label>

    <input
      :id="inputData.name"
      :type="inputData.type"
      :placeholder="inputData.placeholder"
      :value="modelValue"
      @input="handleInput"
      class="input"
    />
    <span :class="{showError:showError}"  v-if="inputData.errorMessage">{{ inputData.errorMessage }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const showError = ref(false);
interface InputData {
  name: string;
  label: string;
  type?: string;
  placeholder: string;
  onInput?: (value: string) => Boolean;
  errorMessage?: string;
}

const props = defineProps({
  inputData: {
    type: Object as () => InputData,
    required: true
  },
  modelValue: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const updateValue = (event: Event) => {
  emit('update:modelValue', (event.target as HTMLInputElement).value);
};

const handleInput = (event: Event) => {
  updateValue(event);
  const value = (event.target as HTMLInputElement).value;
  if(props.inputData.onInput?.(value))showError.value=true;
  else showError.value=false;
};
</script>

<style scoped lang="scss">
@use "@/assets/style" as *;
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
span{
  position: relative;
}
.showError
{
  display: block;
}
</style>
