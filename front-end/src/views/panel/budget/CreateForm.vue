<script lang="ts" setup>
import { ref } from "vue";
import {Section, Form, HeaderSection} from "@/components";
import { useFormStore,useTripStore } from "@/stores";
import { FormType } from "@/types/enum";
import { useRoute } from "vue-router";
const { getFormInputs, isFormValid } = useFormStore();
const {tripMutationBudget} = useTripStore();
const inputs = ref(getFormInputs(FormType.BUDGET));

const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map(input => [input.name, ""]))
);
const route = useRoute();

const handleSubmit = (_formData: any, config: any) => {
  if (config?.send && isFormValid(FormType.BUDGET, formValues.value)) {
    const data = {
        amount: formValues.value?.amount,
        currency: formValues.value?.currency,
        trip: Number(route?.params?.tripId)
      }
      try {
        tripMutationBudget.mutateAsync(data);
      } catch (error) {
      
    }
  }
};
</script>

<template>
  <Section>
    <template #title>
      <header-section
          no-sub-title
          center
          title="Zaplanuj budżet na wycieczkę"
      />
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