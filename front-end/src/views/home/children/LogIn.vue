<script lang="ts" setup>
import { ref } from "vue";
import Form from "@/components/Form.vue";
import Section from "@/components/Section.vue";
import { Validator } from "@/utils/validator/validation";
import { usePageStore } from "@/stores/pageContentStore";

const { getSectionTitle, errorMessage } = usePageStore();
const sectionTitle = getSectionTitle("login");

const validator = new Validator(errorMessage()).isEmpty().minLength(6).save();

const inputStyle = {
  color: "var(--primary-color)",
  fontSize: "2rem",
};

interface Input {
  name: string;
  label: string;
  type: string;
  placeholder: string;
  validation: Validator;
  error: string[];
}

const inputs = ref<Input[]>([
  {
    name: "email",
    label: "Podaj Email:",
    type: "text",
    placeholder: "Wprowadź email",
    validation: validator.createNew().email(),
    error: [],
  },
  {
    name: "password",
    label: "Podaj Hasło:",
    type: "password",
    placeholder: "Wprowadź hasło",
    validation: validator,
    error: [],
  },
]);

const formValues = ref<Record<string, string>>(
  Object.fromEntries(inputs.value.map((input) => [input.name, ""]))
);

const validateForm = () => {
  inputs.value.forEach((input) => {
    const value = formValues.value[input.name];
    if (input.validation) {
      const errorList = input.validation.validate(value);
      input.error =  errorList;
    } else {
      input.error = [];
    }
  });

  return inputs.value.every((input) => input.error.length === 0);
};

const handleSubmit = () => {
  if (validateForm()) {
    console.log("Wartości formularza:");
    console.table(formValues.value); 
  } else {
    console.log("Wykryto błędy:");
    const errorFields = inputs.value.map((input) => [input.name,...input.error]);
    console.log(errorFields);
  }
};
</script>

<template>
  <Section class="logIn">
    <template #title>
      <h1 :style="inputStyle">{{ sectionTitle }}</h1>
    </template>
    <template #content>
      <Form
        :submitButtonLabel="sectionTitle"
        :inputs="inputs"
        :formValues="formValues"
        @submitForm="handleSubmit"
      
      />
    </template>
  </Section>
</template>
