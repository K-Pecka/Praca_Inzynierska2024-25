<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Section, Form, HeaderSection } from "@/components";
import { useFormStore, useTripStore } from "@/stores";
import { FormType } from "@/types/enum";
import dayjs from "dayjs";

const route = useRoute();
const id = Number(route.params.tripId);

const { getFormInputs, isFormValid } = useFormStore();
const inputs = ref(getFormInputs(FormType.TRIP));

const formValues = ref<Record<string, string>>(
  Object.fromEntries(inputs.value.map((input) => [input.name, ""]))
);

const { trip: tripStore } = useTripStore();
const { updateTrip, getTripDetails } = tripStore;
const { isLoading_trip, error_trip } = getTripDetails();

const trip = ref(tripStore.getTripDetails().trip);
watch(
  () => trip?.value,
  (newTrip) => {
    if (newTrip) {
      const tripNameInput = inputs.value.find(
        (input) => input.name === "tripName"
      );
      if (tripNameInput) {
        formValues.value.tripName = newTrip?.name ?? "";
        tripNameInput.config = {
          ...tripNameInput.config,
          edit: true,
          label: newTrip?.name
        };
      }
      const tripDatesInput = inputs.value.find(
        (input) => input.name === "tripDates"
      );
      if (tripDatesInput) {
        formValues.value.start_date = newTrip?.start_date ?? "";
        formValues.value.end_date = newTrip?.end_date ?? "";
        tripDatesInput.config = {
          ...tripDatesInput.config,
          edit: true,
          min: dayjs().format("YYYY-MM-DD") ?? "",
          maxDate: newTrip?.end_date ?? "",
        };
      }
    }
  },
  { immediate: true }
);
function handleSubmit(_formData: any, config: any) {
  if (config?.send && isFormValid(FormType.TRIP, formValues.value)) {
    const { tripName, tripDates } = formValues.value;
    const [start_date, end_date] = tripDates.split(" - ");

    const newData = {
      name: tripName,
      start_date: start_date || "",
      end_date: end_date || "",
    };
    updateTrip.mutateAsync({ tripId: String(id), newData });
  }
}
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection title="Edytuj wycieczkę" no-sub-title center />
    </template>

    <template #content>
      <p v-if="isLoading_trip">Ładowanie danych wycieczki...</p>
      <p v-else-if="error_trip && error_trip.message">
        Błąd: {{ error_trip.message }}
      </p>

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
