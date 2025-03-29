<script setup lang="ts">
import {ref, computed} from "vue";
import {useTicketStore} from "@/stores/trip/useTicketStore";
import AppButton from "@/components/budget/AppButton.vue";
import {VTimePicker} from 'vuetify/labs/VTimePicker'
import {VDateInput} from "vuetify/labs/components";

const emit = defineEmits(["submitTicket", "cancelForm"]);

const store = useTicketStore();


const form = ref({
  type: "Atrakcja",
  name: "",
  date: null,
  time: "",
  assignedTo: null,
  file: null as File | null,
});

const ticketTypeOptions = computed(() => {
  return store.ticketTypes.map((t) => ({
    value: t.value,
    text: t.label,
  }));
});

const today = computed(() => new Date().toISOString().split("T")[0]);

function formatDateToYYYYMMDD(date: Date): string {
  return date.toISOString().split("T")[0];
}

function submitTicket() {
  const payload = {
    ...form.value,
    date: form.value.date ? formatDateToYYYYMMDD(form.value.date) : null,
  };
  emit("submitTicket", payload);

  form.value = {
    type: "train",
    name: "",
    date: null,
    time: "",
    assignedTo: null,
    file: null,
  };
}

const timeMenu = ref(false);

</script>

<template>
  <v-card class="ticket-form pa-4 mt-4">
    <v-card-title>Dodaj nowy bilet</v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" sm="6">
          <v-select
              v-model="form.type"
              :items="ticketTypeOptions"
              item-title="text"
              item-value="value"
              label="Typ biletu"
              variant="outlined"
              chips
              bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
              v-model="form.name"
              label="Nazwa"
              variant="outlined"
              :rules="[v => !!v || 'Nazwa biletu jest wymagana']"
              required
              bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="3">
          <v-date-input
              v-model="form.date"
              label="Wybierz datę"
              prepend-icon=""
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              :min="today"
              bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="3">
          <v-text-field
              v-model="form.time"
              :active="timeMenu"
              :focus="timeMenu"
              variant="outlined"
              label="Godzina"
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
                  v-model="form.time"
                  full-width
              >
              </v-time-picker>
            </v-menu>
          </v-text-field>
        </v-col>


        <v-col cols="12" sm="6">
          <v-select
              v-model="form.assignedTo"
              label="Przypisz do osoby (Opcjonalnie)"
              variant="outlined"
              :items="['Jan', 'Anna', 'Piotr']"
              chips
              clearable
              multiple
              bg-color="background"
          />
        </v-col>

        <v-col cols="12" sm="12">
          <v-file-input
              class="custom-file-input"
              v-model="form.file"
              prepend-icon=""
              label="Przeciągnij lub dodaj bilet"
              prepend-inner-icon="mdi-upload"
              show-size
              variant="outlined"
              bg-color="background"
          >
          </v-file-input>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions>
      <v-spacer/>
      <AppButton variant="secondary"
                 @click="$emit('cancelForm')">
        Anuluj
      </AppButton>
      <AppButton variant="primary" @click="submitTicket">
        Dodaj
      </AppButton>
    </v-card-actions>
  </v-card>
</template>


<style scoped lang="scss">
.ticket-form {
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 1rem;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
}
</style>
