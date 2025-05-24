<script lang="ts" setup>
import { ref } from "vue";
import { Section, Form, HeaderSection } from "@/components";
import { useFormStore, useTripStore } from "@/stores";
import { FormType } from "@/types/enum";

const { trip } = useTripStore();
const { createTrip } = trip;

const { initForm, sendForm } = useFormStore();
const init = initForm(FormType.TRIP);
const inputs = ref(init.inputs);
const formValues = ref(init.values);

const handleSubmit = async () => {
  await sendForm({
    data: formValues.value,
    send: async (data: Record<string, string>) => {
      const { tripDates } = formValues.value;
      const [start_date = "", end_date = ""] = (tripDates || "").split(" - ");
      const tripData = {
        name: formValues.value.tripName,
        start_date: start_date || "",
        end_date: end_date || "",
      };
      await createTrip.mutateAsync(tripData);
    },
  });
};
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <Section style="">
    <template #title>
      <HeaderSection
        title="Stwórz wycieczkę"
        subtitle="Zaplanuj swoją wymarzoną wycieczkę"
        :center="true"
      />
    </template>

    <template #content>
      <Form
        :submitButtonLabel="'Stwórz wycieczkę'"
        :inputs="inputs"
        :formValues="formValues"
        @submitForm="handleSubmit"
        :cancel="{ label: 'anuluj',onclick: () => router.go(-1) }"
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
  color: rgba(0, 0, 0, 0.75);
}
p {
  margin: 0 0 2rem 0;
  text-align: center;
}
</style>
