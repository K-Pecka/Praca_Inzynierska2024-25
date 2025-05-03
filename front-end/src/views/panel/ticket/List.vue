<script setup lang="ts">
import {ref} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import {useTicketStore} from "@/stores/trip/useTicketStore";
import {useTripStore} from "@/stores/trip/useTripStore";
import { useDisplay } from 'vuetify'

import TicketForm from "@/components/trip/module/ticket/TicketForm.vue";
import AppButton from "@/components/budget/AppButton.vue";
import {useUtilsStore} from "@/stores";
import HeaderSection from "@/components/common/HeaderSection.vue";

const {combineDateAndTime} = useUtilsStore();
const route = useRoute();
const tripId = route.params.tripId as string;

const {createTicket} = useTicketStore();
const {data: tickets, isLoading} = useTripStore().getTickets();

const showForm = ref(false);
async function handleAddTicket(newTicketData: {
  type: string;
  name: string;
  date: string;
  time: string;
  assignedTo?: string[];
  file: File;
}) {
  const formData = new FormData();
  formData.append("type", newTicketData.type);
  formData.append("trip", tripId);
  formData.append("valid_from", combineDateAndTime(newTicketData.date, newTicketData.time));
  formData.append("file", newTicketData.file);
  try {
    await createTicket(formData);
    showForm.value = false;
  } catch (error) {
    console.error("Błąd podczas tworzenia biletu:", error);
  }
}

const downloadFile = (ticket: string) => {
  const link = document.createElement('a');
  link.href = ticket;
  link.download = 'bilet.pdf';
  link.click();
}

const filteredTickets = () => {
  return (
      tickets.value?.filter((ticket) => ticket.trip === Number(tripId)) ?? []
  );
};

const toggleForm = () => {
  showForm.value = !showForm.value;
};

</script>

<template>
  <Section>
    <template #title>
      <HeaderSection subtitle="Bilety" button button-text="Dodaj Bilet" :button-action="toggleForm" />
    </template>

    <template #content>
      <v-col cols="12">
        <TicketForm
            v-if="showForm"
            @submitTicket="handleAddTicket"
            @cancelForm="showForm = false"
            class="form-container"
        />
      </v-col>

      <!-- Ticket cards -->
      <v-col cols="12">

        <!-- Empty state when no tickets are present -->
        <v-row
            v-if="isLoading && tickets && tickets.length === 0"
            class="background-secondary"
        >
          <v-icon size="48" color="black"
          >mdi-ticket-confirmation-outline
          </v-icon>
          <p>Brak dodanych biletów</p>
          <a class="color-primary" @click="showForm = true">
            Dodaj pierwszy bilet
          </a>
        </v-row>
        <!-- Loaded tickets -->
        <v-card
            class="background-secondary rounded-xl"
            v-else-if="tickets && tickets.length > 0"
            v-for="ticket in filteredTickets().reverse()"
            :key="ticket.id"
            elevation="4"
        >
          <!-- Ticket card header -->
          <v-card-text>
            <v-sheet elevation="0" color="transparent" class="d-flex justify-center">
              <v-icon class="color-text" large size="70px"> mdi-download</v-icon>
              <v-row no-gutters class="flex-column justify-center pl-4">
                <span class="color-text font-weight-bold text-h5">{{ ticket.name }}</span>
                <span class="color-primary text-h6 font-weight-medium"
                      v-if="ticket.valid_from_date && ticket.valid_from_time">
                  {{ ticket.valid_from_time }} {{ ticket.valid_from_date }}
                </span>
              </v-row>
            </v-sheet>
            <v-divider class="my-4 mx-2" />
            <!-- Ticket card body -->
            <v-card-actions class="justify-space-between flex-wrap">
              <v-select
                  :items="['Jan', 'Anna', 'Piotr']"
                  label="Przypisz do osoby (Opcjonalnie)"
                  variant="outlined"
                  multiple
                  density="compact"
                  bg-color="background"
                  max-width="600px"
                  min-width="200px"
                  rounded="lg"
              />

              <!-- Button to download the ticket -->
              <AppButton
                  variant="primary"
                  @click="() => downloadFile(ticket.file)"
                  height-auto
                  font-auto
                  text="Pobierz bilet"
              >
                <v-icon>mdi-download</v-icon>
              </AppButton>
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-col>
    </template>
  </Section>
</template>

<style lang="scss">
.v-select .v-input__details {
  position: absolute;
}
</style>
