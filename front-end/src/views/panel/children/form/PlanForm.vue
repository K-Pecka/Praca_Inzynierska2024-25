<script lang="ts" setup>
import { ref } from "vue";
import {Section,Form} from "@/components";
import { useFormStore,useTripStore } from "@/stores";
import { FormType } from "@/type/enum";
import { useRoute } from "vue-router";
import { Plan } from "@/type/interface";

const { planMutationAdd } = useTripStore();
const { getFormInputs, isFormValid } = useFormStore();

const inputs = ref(getFormInputs(FormType.PLAN));
const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map(input => [input.name, ""]))
);

const route = useRoute();
const id = Number(Array.isArray(route.params.tripId) ? route.params.tripId[0] : route.params.tripId);
const handleSubmit = (_formData: any, config: any) => {
  if (config?.send && isFormValid(FormType.PLAN, formValues.value)) {
    const { tripName, city,tripDates } = formValues.value;
    const [start_date, end_date] = tripDates.split(' - ');
    const newPlan:Plan = {
      id: id,
      name: tripName,
      country: city,
      start_date: start_date || '',
      end_date: end_date || ''
    };
    try {
      planMutationAdd.mutateAsync({ data: newPlan, tripId: id });
    } catch (error) {
      
    }
  }
};
</script>

<template>
  <Section>
    <template #title>
      <h1>Stwórz swój idealny plan</h1>
      <p>elastyczny harmonogram wymarzonej podróży</p>
    </template>

    <template #content>
      <Form
          :submitButtonLabel="'Stwórz plan podróży'"
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