<script lang="ts" setup>
import { ref, watch } from "vue";
import {Section, Form, HeaderSection} from "@/components";
import { useFormStore,useTripStore, useUtilsStore } from "@/stores";
import { FormType } from "@/types/enum";
import { Plan } from "@/types/interface";

const { plan } = useTripStore();
const {addPlan} = plan;
const { getFormInputs, isFormValid } = useFormStore();

const {trip:tripStore} = useTripStore();
const {getTripDetails} = tripStore;
const {trip} = getTripDetails();
const {getTripId} = useUtilsStore()
const inputs = ref(getFormInputs(FormType.PLAN));
const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map(input => [input.name, ""]))
);
watch(trip,() => {
  if(trip){
    const tripDatesInput = inputs.value.find(input => input.name === 'tripDates');

    if (tripDatesInput && tripDatesInput.config) {
      tripDatesInput.config = {
        ...tripDatesInput.config,
        min: trip.value?.start_date,
        max: trip.value?.end_date
      };
    }
  }
});


const handleSubmit = (_formData: any, config: any) => {
  if (config?.send && isFormValid(FormType.PLAN, formValues.value)) {
    const { tripName, city,tripDates } = formValues.value;
    const [start_date, end_date] = tripDates.split(' - ');
    //console.log(trip?.value);
    const newPlan:Plan = {
      name: tripName,
      country: city,
      start_date: start_date || '',
      end_date: end_date || ''
    };
    try {
      addPlan.mutateAsync({ data: newPlan, tripId: getTripId() });
    } catch (error) {
      
    }
  }
};
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection
          title="Stwórz swój idealny plan"
          no-sub-title
          center
      />
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