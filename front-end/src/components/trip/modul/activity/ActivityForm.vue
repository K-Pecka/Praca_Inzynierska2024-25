<script setup lang="ts">
import { ref } from "vue";
import AppButton from "@/components/budget/AppButton.vue";
import { VTimePicker } from "vuetify/labs/VTimePicker";
import { defineEmits } from "vue";

const emit = defineEmits(["submitActivity", "cancelForm"]);

const form = ref({
  type: "Zwiedzanie",
  name: "",
  start_time: "",
  duration: "",
  location: "",
  assignedTo: "",
  description: "",
});

const timeMenu = ref(false);

function submitActivity() {
  emit("submitActivity", { ...form.value });
  form.value = {
    type: "tour",
    name: "",
    start_time: "",
    duration: "",
    location: "",
    assignedTo: "",
    description: "",
  };
}
</script>

<template>
  <v-card class="activity-form pa-4 mt-4">
    <v-card-title>Dodaj nową aktywność</v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" sm="6">
          <v-select
              v-model="form.type"
              :items="['Zwiedzanie', 'Jedzenie', 'Sport', 'Relaks']"
              label="Typ aktywności"
              variant="outlined"
              chips
              bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
              v-model="form.name"
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
                  full-width
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
              v-model="form.assignedTo"
              label="Wybierz bilet"
              variant="outlined"
              :items="['Bilet A', 'Bilet B', 'Bilet C']"
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
      <AppButton variant="secondary" @click="$emit('cancelForm')">
        Anuluj
      </AppButton>
      <AppButton variant="primary" @click="submitActivity">
        Dodaj
      </AppButton>
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">
.activity-form {
  background-color: rgb(var(--v-theme-background));
  border-radius: 1rem;
  box-shadow: 0 0px 0px rgba(0, 0, 0, 0);
}
</style>
