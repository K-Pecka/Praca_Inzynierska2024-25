<template>
  <div class="form-container">
    <div class="wrapper">
      <form @submit.prevent="handleSubmit">
        <div v-for="(inputData, index) in inputs" :key="index">
          <InputWithLabel
            :inputData="inputData"
            v-model="formValues[inputData.name]"
            @update="handleFieldUpdate"
          />
        </div>
        <button type="submit">{{ submitButtonLabel }}</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import InputWithLabel from "@/components/InputWithLabel.vue";
import { ref } from "vue";

interface InputData {
  name: string;
  label: string;
  placeholder: string;
  validation: any;
  error: string[];
}

const props = defineProps<{
  inputs: InputData[];
  formValues: Record<string, string>;
  submitButtonLabel: string | undefined;
}>();

const emit = defineEmits(["submitForm"]);

const handleFieldUpdate = (name: string, value: string) => {
  props.formValues[name] = value;

  const input = props.inputs.find(input => input.name === name);
  if (input) {
    input.error = input.validation.validate(value);
  }
  emit("submitForm", props.formValues);
};

const handleSubmit = () => {
  emit("submitForm", props.formValues, { send: true });
};
</script>

<style scoped>
.form-container {
  width: 50%;
  margin: auto;
  background-color: rgba(var(--rgb-secondary-color), 0.9);
  padding: 0.25rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
}

button {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  width: 100%;
  padding: 1rem;
  border: none;
  cursor: pointer;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
}
</style>
