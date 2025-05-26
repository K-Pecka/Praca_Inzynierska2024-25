<script lang="ts" setup>
import { ref } from "vue";
import {Section, Form, HeaderSection} from "@/components";
import { Input,Register } from "@/types/interface";
import { FormType } from "@/types/enum";
import { useAuthStore,useFormStore,usePageHomeStore } from "@/stores";

const { getSectionTitle } = usePageHomeStore();
const { registerMutation } = useAuthStore();
const { getFormInputs, isFormValid } = useFormStore();

const sectionTitle = getSectionTitle(FormType.REGISTER);
const inputs = ref<Input[]>(getFormInputs(FormType.REGISTER));
const formValues = ref<Record<string, string>>(
  Object.fromEntries(
    inputs.value.map((input: { name: string }) => [input.name, ""])
  )
);

const handleSubmit = async (event: Event, config: { send: boolean }) => {
  event.preventDefault();

  console.log("Submitting form:", formValues.value);

  if (config?.send && isFormValid(FormType.REGISTER, formValues.value)) {
    const { pass_2, ...registrationData } = formValues.value;

    try {
      await registerMutation.mutateAsync(registrationData as unknown as Register);
      console.log("Registration successful");
    } catch (error) {
      console.error("Registration error:", error);
    }

    Object.keys(formValues.value).forEach(key => {
      formValues.value[key] = '';
    });
  } else {
    console.log("Form invalid or config.send is false");
  }
};
</script>

<template>
  <Section class="logIn gradient-text">
    <template #title>
      <HeaderSection no-sub-title :title-gradient-text="sectionTitle" center />
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



<style scoped lang="scss">
h1 {
  font-size: 2rem;
}
.container {
  width: 50%;
  margin: auto;
}
.form-container {
  width: 100%;
  background-color: rgb(var(--v-theme-secondary), 0.9);
  margin: auto;
  padding: 0.25rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
}
.extraOption a {
  color: rgb(var(--v-theme-text));
}
.extraOption div {
  margin: 2rem auto;
}
.wrapper {
  padding: 2rem;
}
button {
  background-color: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-secondary));
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
