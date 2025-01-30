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

<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import Section from "@/components/Section.vue";
import Form from "@/components/Form.vue";
import { Validator } from "@/utils/validator/validation";
import { usePageStore } from "@/stores/pageContentStore";

const { getSectionTitle, errorMessage } = usePageStore();
const sectionTitle = getSectionTitle("register");

const validator = new Validator({...errorMessage(),...{isEqual:"Hasła muszą być takie same"}}).isEmpty().minLength(6).save();

const inputStyle = {
  color: "var(--primary-color)",
  fontSize: "2rem",
};

interface Config {
  required: boolean;
}
interface Input {
  name: string;
  related?: string[];
  label: string;
  type: string;
  placeholder: string;
  validation: Validator;
  config?: Config,
  error: string[];
}

const inputs = ref<Input[]>([
  {
    name: "name",
    label: "Podaj Imie:",
    type: "text",
    placeholder: "Wprowadź imie",
    validation: validator.createNew().minLength(3),
    config:{required:true},
    error: [],
  },
  {
    name: "surname",
    label: "Podaj Nazwisko:",
    type: "text",
    placeholder: "Wprowadź nazwisko",
    validation: validator.createNew().minLength(3),
    config:{required:true},
    error: [],
  },
  {
    name: "email",
    label: "Podaj e-mail:",
    type: "email",
    placeholder: "Wprowadź e-mail",
    validation: validator.createNew().email(),
    config:{required:true},
    error: [],
  },
  {
    name: "pass_1",
    related:["pass_2"],
    label: "Podaj hasło:",
    type: "text",
    placeholder: "Wprowadź hasło",
    validation: validator,
    config:{required:true},
    error: [],
  },
  {
    name: "pass_2",
    related:["pass_1"],
    label: "Podaj ponownie hasło:",
    type: "text",
    placeholder: "Wprowadź hasło",
    validation: validator,
    config:{required:true},
    error: [],
  },
]);
const formValues = ref<Record<string, string>>(
  Object.fromEntries(inputs.value.map((input) => [input.name, ""]))
);


const validateForm = computed(() => {
  return inputs.value
    .map((input) => {
      const value = formValues.value[input.name];
      input.error = input.validation ? input.validation.validate(value) : [];
      return input.error.length === 0;
    })
    .every(Boolean);
});

const handleSubmit = (_: any, config: any) => {
  if (config?.send && validateForm.value) {
    console.log("Wartości formularza:");
    console.table(formValues.value);
  } else {
    // console.log("Wykryto błędy:");
    // const errorFields = inputs.value.map((input) => [
    //   input.name,
    //   ...input.error,
    // ]);
    // console.log(errorFields);
  }
};
</script>

<style scoped lang="scss">
.container {
  width: 50%;
  margin: auto;
}
.form-container {
  width: 100%;
  background-color: rgba(var(--rgb-secondary-color), 0.9);
  margin: auto;
  padding: 0.25rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
}
.extraOption a {
  color: var(--text-color);
}
.extraOption div {
  margin: 2rem auto;
}
.wrapper {
  padding: 2rem;
}
button {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: auto;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  border: none;
  padding: 1rem;
  cursor: pointer;
}
.more-action {
  img {
    width: 1.5rem;
    height: 1.5rem;
    padding: 0.25rem;
  }
}

.error-message {
  color: red;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
</style>
