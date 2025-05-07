<script setup lang="ts">
import { ref, computed, watchEffect } from "vue";
import AppButton from "@/components/AppButton.vue";
import { VTimePicker } from 'vuetify/labs/VTimePicker'
import { VDateInput } from "vuetify/labs/components";
import { ticketCategory } from "@/data/category/ticket";
import { User } from "@/types";
const emit = defineEmits(["submitTicket", "cancelForm"]);

const form = ref({
  type: ticketCategory[0].text,
  name: "",
  date: null,
  time: "",
  assignedTo: null,
  file: null as File | null,
});

const ticketTypeOptions = computed(() => ticketCategory);

const today = computed(() => new Date().toISOString().split("T")[0]);

function formatDateToYYYYMMDD(date: Date): string {
  return date.toISOString().split("T")[0];
}

function submitTicket() {
  const payload = {
    ...form.value,
    date: form.value.date ? formatDateToYYYYMMDD(form.value.date) : new Date("YYYY-MM-DD").getDate(),
  };
  //console.log("Payload", payload);
  emit("submitTicket", payload);

  form.value = {
    type: ticketCategory[0].text,
    name: "",
    date: null,
    time: "",
    assignedTo: null,
    file: null,
  };
}

const timeMenu = ref(false);

defineProps<{
  members: {name:string,userId:number}[];
}>();
</script>

<template>
  <v-card
      class="pa-4 mt-4 background-secondary rounded-lg"
      elevation="4"
  >
    <v-card-title>Dodaj nowy bilet</v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" lg="6" md="6" class="tight-col">
          <v-select
              v-model="form.type"
              :items="ticketTypeOptions"
              item-title="text"
              item-value="value"
              label="Typ biletu"
              variant="outlined"
              bg-color="background"
              density="comfortable"
          />
        </v-col>

        <v-col cols="12" lg="6" md="6" class="tight-col">
          <v-text-field
              v-model="form.name"
              label="Nazwa"
              variant="outlined"
              :rules="[v => !!v || 'Nazwa biletu jest wymagana']"
              required
              bg-color="background"
              density="comfortable"
          />
        </v-col>

        <v-col cols="12" lg="3" md="6" class="tight-col">
          <v-date-input
              v-model="form.date"
              label="Wybierz datę"
              prepend-icon=""
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              :min="today"
              bg-color="background"
              density="comfortable"
          />
        </v-col>

        <v-col cols="12" lg="3" md="6" class="tight-col">
          <v-text-field
              v-model="form.time"
              :active="timeMenu"
              :focus="timeMenu"
              variant="outlined"
              label="Godzina"
              prepend-inner-icon="mdi-clock-time-four-outline"
              readonly
              bg-color="background"
              density="comfortable"
          >
            <v-menu
                v-model="timeMenu"
                :close-on-content-click="false"
                activator="parent"
                transition="scale-transition"
                density="comfortable"
            >
              <v-time-picker
                  v-if="timeMenu"
                  v-model="form.time"
                  format="24hr"
                  scrollable
              >
              </v-time-picker>
            </v-menu>
          </v-text-field>
        </v-col>

        <v-col cols="12" lg="6" md="12" class="tight-col">
          <v-select
              v-model="form.assignedTo"
              label="Przypisz do osoby (Opcjonalnie)"
              variant="outlined"
              :disabled="members.length === 0"
              :items="members"
              item-title="name"
              item-value="userId"
              chips
              clearable
              multiple
              bg-color="background"
              density="comfortable"
          />
        </v-col>

        <v-col cols="12" lg="12" class="tight-col">
          <v-file-input
              class="custom-file-input"
              v-model="form.file"
              prepend-icon=""
              label="Przeciągnij lub dodaj bilet"
              prepend-inner-icon="mdi-upload"
              show-size
              variant="outlined"
              bg-color="background"
              density="comfortable"
          >
          </v-file-input>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions class="form-actions">
      <AppButton
          color="accent"
          text="Anuluj"
          @click="$emit('cancelForm')"
      />
      <AppButton
          color="primary"
          text="Dodaj"
          @click="submitTicket"
      />
    </v-card-actions>
  </v-card>
</template>


<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.form-actions {
  gap: 1rem;
  display: flex;
  justify-content: flex-end;
  @media (max-width: 600px) {
    flex-wrap: wrap;
    justify-content: center;
  }
}

.tight-col {
  padding: 0.25rem !important;
}


</style>
