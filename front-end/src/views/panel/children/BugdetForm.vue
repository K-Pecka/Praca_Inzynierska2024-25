<script lang="ts" setup>
import { ref } from "vue";
import Section from "@/components/Section.vue";
import Form from "@/components/Form.vue";
import { useFormStore } from "@/stores/formStore";
import { FormType } from "@/type/interface";

const { getFormInputs, validateForm } = useFormStore();

const inputs = ref(getFormInputs(FormType.BUDGET));

const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map(input => [input.name, ""]))
);


const handleSubmit = (_formData: any, config: any) => {
  if (config?.send && validateForm(FormType.PLAN, formValues.value)) {
    console.log("Plan został utworzony. Dane:", formValues.value);
  }
};
</script>

<template>
  <Section>
    <template #title>
      <h1>Zaplanuj budżet na wycieczkę</h1>
    </template>

    <template #content>
      <Form
          :submitButtonLabel="'Zaplanuj budżet'"
          :inputs="inputs"
          :formValues="formValues"
          @submitForm="handleSubmit"
      >
      </Form>
    </template>
  </Section>
</template>

<style lang="scss" scoped>
h1 {
  color: rgb(var(--v-theme-primary));
  font-size: 2rem;
  margin-bottom: 0.5rem;
}
p {
  margin: 0 0 2rem 0;
  text-align: center;
}
</style>