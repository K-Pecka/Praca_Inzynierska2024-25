<script lang="ts" setup>
import { ref } from "vue";
import Section from "@/components/Section.vue";
import Form from "@/components/Form.vue";
import { useFormStore } from "@/stores/ui/useFormStore";
import { FormType } from "@/type/enum";
import { useTripStore } from "@/stores/tripStore";
import { useRoute } from "vue-router";
import { Plan } from "@/type/interface";

const { planMutationAdd } = useTripStore();
const { getFormInputs, isFormValid } = useFormStore();

const inputs = ref(getFormInputs(FormType.PLAN));
const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map(input => [input.name, ""]))
);

const route = useRoute();
const id = Array.isArray(route.params.tripId) ? route.params.tripId[0] : route.params.tripId;
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
      console.log(id);
      planMutationAdd.mutateAsync({ data: newPlan, tripId: id });
    } catch (error) {
      console.log("ERROR");
    }
    console.log("Plan został utworzony. Dane:", formValues.value);
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