<script setup lang="ts">
import {ref, watch} from "vue";
import {useRoute} from "vue-router";
import {Section, Form} from "@/components";
import {useFormStore, useTripStore} from "@/stores";
import {FormType} from "@/type/enum";

const route = useRoute();
const id = route.params.tripId as string;

const { getFormInputs, isFormValid } = useFormStore();
const inputs = ref(getFormInputs(FormType.TRIP));

const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map((input) => [input.name, ""]))
);

const { getTripDetails, tripMutationUpdate } = useTripStore();
const { data: tripData, isLoading, error } = getTripDetails(id);

watch(
    () => tripData.value,
    (trip) => {
      if (trip) {
        formValues.value.tripName = trip.name;
        formValues.value.tripDates = `${trip.start_date} - ${trip.end_date}`;
      }
    },
    { immediate: true }
);

function handleSubmit(_formData: any, config: any) {
  if (config?.send && isFormValid(FormType.TRIP, formValues.value)) {
    const { tripName, tripDates } = formValues.value;
    const [start_date, end_date] = tripDates.split(' - ');

    const newData = {
      name: tripName,
      start_date: start_date || '',
      end_date: end_date || '',
    };
    tripMutationUpdate.mutateAsync({ tripId: id, newData });
  }
}
</script>

<template>
  <Section>
    <template #title>
      <h1>Edytuj wycieczkę</h1>
      <p>Zmodyfikuj nazwę i daty wycieczki</p>
    </template>

    <template #content>
      <p v-if="isLoading">Ładowanie danych wycieczki...</p>
      <p v-else-if="error">Błąd: {{ error.message }}</p>

      <Form
          v-else
          :submitButtonLabel="'Zapisz zmiany'"
          :inputs="inputs"
          :formValues="formValues"
          @submitForm="handleSubmit"
      />
    </template>
  </Section>
</template>

<style scoped lang="scss">
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