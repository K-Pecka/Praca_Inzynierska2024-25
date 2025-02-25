<script setup lang="ts">
import {ref, computed} from "vue";
import {defineEmits} from "vue";
import {useTicketStore} from "@/stores/useTicketStore";

const emit = defineEmits(["submitTicket", "cancelForm"]);

const store = useTicketStore();


const form = ref({
  type: "transport",
  name: "",
  date: "",
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
    type: "transport",
    name: "",
    date: "",
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
              outlined
              dense
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
              v-model="form.name"
              label="Nazwa"
              outlined
              dense
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
              v-model="form.date"
              label="Data (dd.mm.rrrr)"
              placeholder="dd.mm.rrrr"
              outlined
              dense
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
              v-model="form.assignedTo"
              label="Przypisz do osoby (Opcjonalnie)"
              outlined
              dense
          />
        </v-col>

        <v-col cols="12">
          <v-file-input
              v-model="form.file"
              prepend-icon="mdi-upload"
              label="Przeciągnij lub dodaj bilet"
              show-size
              outlined
              dense
          />
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions>
      <v-spacer/>
      <v-btn color="primary" @click="submitTicket">
        Dodaj Bilet
      </v-btn>
      <v-btn color="secondary" @click="$emit('cancelForm')">
        Anuluj
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<style scoped lang="scss">
.ticket-form {
  background-color: rgb(var(--v-theme-secondary), 0.2);
  border-radius: 1rem;
}
</style>
