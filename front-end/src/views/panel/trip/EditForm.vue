<script setup lang="ts">
import {ref, watch} from "vue";
import {useRoute} from "vue-router";
import {Section, Form} from "@/components";
import {useFormStore, useTripStore} from "@/stores";
import {FormType} from "@/types/enum";

const route = useRoute();
const id = Number(route.params.tripId);

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
      const tripDatesInput = inputs.value.find(
          (input) => input.name === "tripDates"
      );
      if (tripDatesInput) {
        formValues.value.tripName = trip?.name ?? '';
        formValues.value.start_date = trip?.start_date ?? '';
        formValues.value.end_date = trip?.end_date ?? '';
        if (tripDatesInput) {

          tripDatesInput.config = {
            ...tripDatesInput.config,
            edit: true,
            min: trip?.start_date ?? '',
            max: trip?.end_date ?? '',
          };
          console.log(tripDatesInput.config.min, tripDatesInput.config.max);
        }
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
    tripMutationUpdate.mutateAsync({ tripId: String(id), newData });
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