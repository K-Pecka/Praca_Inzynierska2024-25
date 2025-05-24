<script lang="ts" setup>
import { ref } from "vue";
import {Section, Form, HeaderSection} from "@/components";
import { Input,Register } from "@/types/interface";
import { FormType } from "@/types/enum";
import { useAuthStore,useFormStore,usePageHomeStore } from "@/stores";

const { getSectionTitle } = usePageHomeStore();
const { registerMutation } = useAuthStore();
const { initForm,sendForm } = useFormStore();

const sectionTitle = getSectionTitle(FormType.REGISTER);
const init = initForm(FormType.REGISTER);
const inputs = ref(init.inputs);
const formValues = ref(init.values);

const handleSubmit = async () => {
  await sendForm({
    data: formValues.value,
    send: async (data) => {
      const { pass_2, ...registrationData } = data;
      await registerMutation.mutateAsync(registrationData as Register);
    }
  });
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
