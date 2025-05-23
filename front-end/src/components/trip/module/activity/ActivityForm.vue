<script setup lang="ts">
import { computed, ref } from "vue";
import {useActivityStore} from "@/stores/trip/useActivityStore";
import AppButton from "@/components/AppButton.vue";
import { VTimePicker } from "vuetify/labs/VTimePicker";
import { useTicketStore } from "@/stores";

const emit = defineEmits(["submitActivity", "cancelForm"]);

const form = ref({
  type: 1,
  name: "",
  start_time: "",
  duration: "",
  location: "",
  description: "",
  ticket:""
});

const timeMenu = ref(false);

const nameRules = [(v: string) => !!v || "Nazwa aktywności jest wymagana"];

const isFormValid = computed(() => form.value.name.trim() !== "");

function submitActivity() {
  if (!isFormValid.value) {
    alert("Uzupełnij nazwę aktywności.");
    return;
  }
 const payload = Object.fromEntries(
    Object.entries(form.value).filter(([key, value]) => !(key === 'ticket' && value === ''))
  );
  emit("submitActivity", { ...payload });
  form.value = {
    type: 1,
    name: "",
    start_time: "",
    duration: "",
    location: "",
    description: "",
    ticket:""
  };
}
const { activityTypes } = useActivityStore();

const {getTickets} = useTicketStore()
const {data:tickets} = getTickets();

const ticketsItems = computed(() =>{
  return (tickets.value || []).map((t) => ({
    title: t.name,
    value: t.id,
  }))
});
  
</script>

<template>
  <v-card class="activity-form pa-4 mt-4" elevation="0">
    <v-card-title>Dodaj nową aktywność</v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" sm="6">
          <v-select
            v-model="form.type"
            :items="activityTypes"
            label="Typ aktywności"
            variant="outlined"
            bg-color="background"
            item-value="id"
            item-title="name"
          >
          </v-select>
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
            :active="timeMenu"
            :focus="timeMenu"
            variant="outlined"
            label="Godzina rozpoczęcia"
            prepend-inner-icon="mdi-clock-time-four-outline"
            readonly
            bg-color="background"
          >
            <v-menu
              v-model="timeMenu"
              :close-on-content-click="false"
              activator="parent"
              transition="scale-transition"
            >
              <v-time-picker
                v-if="timeMenu"
                v-model="form.start_time"
                format="24hr"
                scrollable
                :actions="true"
              />

            </v-menu>
          </v-text-field>
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
            v-model="form.duration"
            label="Czas trwania (min)"
            variant="outlined"
            type="number"
            bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
            v-model="form.location"
            label="Miejsce"
            variant="outlined"
            bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-select
            v-model="form.ticket"
            label="Wybierz bilet"
            variant="outlined"
            :items="ticketsItems"
            bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="12">
          <v-textarea
            v-model="form.description"
            label="Opis"
            variant="outlined"
            bg-color="background"
          />
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <AppButton
          color="accent"
          text="Anuluj"
          @click="$emit('cancelForm')"
      />
      <AppButton
          color="primary"
          text="Dodaj"
          @click="submitActivity"
          :disabled="!isFormValid"
      />
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">
.activity-form {
  background-color: rgb(var(--v-theme-background));
  border-radius: 1rem;
}
</style>
