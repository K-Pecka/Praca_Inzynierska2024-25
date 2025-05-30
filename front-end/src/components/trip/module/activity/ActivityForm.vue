<script setup lang="ts">
import { computed, ref } from "vue";
import { useActivityStore } from "@/stores/trip/useActivityStore";
import AppButton from "@/components/AppButton.vue";
import { useTicketStore } from "@/stores";

const emit = defineEmits(["submitActivity", "cancelForm"]);

const formRef = ref();
const isFormValid = ref(false);
const hasError = ref(false);

const form = ref({
  type: 1,
  name: "",
  start_time: "",
  duration: 0,
  location: "",
  description: "",
  ticket: ""
});

const nameRules = [(v: string) => !!v || "Nazwa aktywności jest wymagana"];
const timeRules = [
  (value: string) => {
    if (!value) return "Godzina jest wymagana";
    const timeRegex = /^(?:([0-9])|([01]\d|2[0-3])):([0-5]\d)$/;
    return timeRegex.test(value) || "Podaj godzinę w formacie HH:MM w systyemie 24H";
  }
];
const durationRules = [
  (v: string) => !v || !isNaN(Number(v)) || "Podaj poprawny czas trwania",
  (v: string) => {
  const num = Number(v);
  return num <= 1000 || "Maksymalna wartość to 1000 min";
  },
  (v: string) => !isNaN(Number(v)) && Number(v)>=0 || "Czas trwania nie może być mniejszy niż 0",
  (v: string) => /^\d+$/.test(v) || "Podaj poprawną liczbę całkowitą",
];

async function submitActivity() {
 const isValid = await formRef.value?.validate?.();
  if (!isValid) {
    hasError.value = true;
    return;
  }
  hasError.value = false;

  const payload = Object.fromEntries(
    Object.entries(form.value).filter(([key, value]) => !(key === "ticket" && value === ""))
  );
  emit("submitActivity", { ...payload });
}

const { activityTypes } = useActivityStore();
const { getTickets } = useTicketStore();
const { data: tickets } = getTickets();
import {activity} from "@/data/category/activity"
const activityTypesList = computed(()=>{
  if(activityTypes.length>0) return activityTypes;
  return activity
})
const ticketsItems = computed(() => {
  return (tickets.value || []).map((t) => ({
    title: t.name,
    value: t.id
  }));
});
</script>

<template>
  <v-form ref="formRef" v-slot="{ isValid }" v-model="isFormValid">
    <v-card class="activity-form pa-4 mt-4" elevation="0">
      <v-card-title>Dodaj nową aktywność</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <v-select
              v-model="form.type"
              :items="activityTypesList"
              label="Typ aktywności"
              variant="outlined"
              bg-color="background"
              item-value="id"
              item-title="name"
            />
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.name"
              :rules="nameRules"
              label="Nazwa aktywności"
              variant="outlined"
              required
              bg-color="background"
            />
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.start_time"
              variant="outlined"
              label="Godzina rozpoczęcia"
              bg-color="background"
              placeholder="hh:mm"
              :rules="timeRules"
              maxlength="5"
            />
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.duration"
              label="Czas trwania (min)"
              variant="outlined"
              type="number"
              bg-color="background"
              :rules="durationRules"
            />
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.location"
              label="Miejsce"
              variant="outlined"
              bg-color="background"
              :rules="nameRules"
            />
          </v-col>

          <v-col cols="12" sm="6">
            <v-select
              v-model="form.ticket"
              :disabled="ticketsItems.length === 0"
              label="Wybierz bilet"
              variant="outlined"
              :items="ticketsItems"
              bg-color="background"
              clearable
            />
          </v-col>

          <v-col cols="12">
            <v-textarea
              v-model="form.description"
              label="Opis"
              variant="outlined"
              bg-color="background"
              :rules="nameRules"
            />
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <AppButton color="accent" text="Anuluj" @click="$emit('cancelForm')" />
        <AppButton
          color="primary"
          text="Dodaj"
          @click="submitActivity"
          :disabled="!isFormValid"
        />
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<style scoped lang="scss">
.activity-form {
  background-color: rgb(var(--v-theme-background));
  border-radius: 1rem;
}
</style>
