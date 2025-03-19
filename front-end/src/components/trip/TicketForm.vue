<script setup lang="ts">
import {ref, computed} from "vue";
import {useTicketStore} from "@/stores/trip/useTicketStore";
import AppButton from "@/components/budget/AppButton.vue";

const emit = defineEmits(["submitTicket", "cancelForm"]);

const store = useTicketStore();


const form = ref({
  type: "Atrakcja",
  name: "",
  date: "",
  hour: "",
  assignedTo: "",
  file: null as File | null,
});

const ticketTypeOptions = computed(() => {
  return store.ticketTypes.map((t) => ({
    value: t.value,
    text: t.label,
  }));
});

function submitTicket() {
  emit("submitTicket", {...form.value});

  form.value = {
    type: "train",
    name: "",
    date: "",
    hour: "",
    assignedTo: "",
    file: null,
  };
}
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
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
              v-model="form.name"
              label="Nazwa"
              variant="outlined"
          />
        </v-col>

        <v-col cols="12" sm="3">
          <v-text-field
              v-model="form.date"
              label="Data (dd.mm.rrrr)"
              placeholder="dd.mm.rrrr"
              variant="outlined"
          />
        </v-col>

        <v-col cols="12" sm="3">
          <v-text-field
              v-model="form.hour"
              label="Godzina (hh:mm)"
              placeholder="hh:mm"
              variant="outlined"
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-select
              v-model="form.assignedTo"
              label="Przypisz do osoby (Opcjonalnie)"
              variant="outlined"
          />
        </v-col>

        <v-col cols="12">
          <v-file-input
              v-model="form.file"
              prepend-icon="mdi-upload"
              label="Przeciągnij lub dodaj bilet"
              show-size
              variant="outlined"
              dense
          />
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
}
</style>
