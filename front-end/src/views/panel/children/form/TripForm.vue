<script lang="ts" setup>
import { ref } from "vue";
import {Section,Form} from "@/components";
import { useFormStore,useTripStore } from "@/stores";
import { FormType } from "@/type/enum";

const { tripMutationAdd } = useTripStore();

const { getFormInputs, isFormValid } = useFormStore();

const inputs = ref(getFormInputs(FormType.TRIP));

const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map(input => [input.name, ""]))
);
const handleSubmit = (_formData: any, config: any) => {
  if (config?.send && isFormValid(FormType.TRIP, formValues.value)) {
    const { tripName, tripDates } = formValues.value;
    const [start_date, end_date] = tripDates.split(' - ');
    const data = {
      name: formValues.value.tripName,
      start_date: start_date || '',
      end_date: end_date || ''
    }
  
    try {
      tripMutationAdd.mutateAsync(data);
    } catch (error) {
      console.log("ERROR");
    }
  }
};
</script>

<template>
  <Section>
    <template #title>
      <h1>Stwórz wycieczkę</h1>
      <p></p>
    </template>

    <template #content>
      <Form
          :submitButtonLabel="'Stwórz wycieczkę'"
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