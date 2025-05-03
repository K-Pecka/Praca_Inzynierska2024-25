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
const { smAndDown } = useDisplay()
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


</script>

<template>
  <Section>
    <template #title>
      <HeaderSection>
        <template #subtitle>
          <v-col cols="12">
            <v-row class="pb-1 justify-space-between" align="center">
              <span>
                Bilety
              </span>
              <AppButton
                  variant="primary"
                  v-if="!showForm"
                  @click="showForm = !showForm"
                  width="200px"
                  height="height-auto"
                  font-size="font-auto"
              >
                Dodaj Bilet
              </AppButton>
            </v-row>
          </v-col>
        </template>
      </HeaderSection>
    </template>

    <template #content>
      <TicketForm
          v-if="showForm"
          @submitTicket="handleAddTicket"
          @cancelForm="showForm = false"
          class="form-container"
      />

      <!-- Ticket cards -->
      <v-col cols="12" class="pa-0">

        <!-- Empty state when no tickets are present -->
        <v-row
            v-if="tickets && tickets.length === 0"
            class="empty-tickets pa-5"
        >
          <v-icon size="48" color="black"
          >mdi-ticket-confirmation-outline
          </v-icon>
          <p class="empty-text">Brak dodanych biletów</p>
          <a class="add-link" @click="showForm = true">
            Dodaj pierwszy bilet
          </a>
        </v-row>
        <!-- Loaded tickets -->
        <v-card
            class="ticket-card rounded-xl px-10 pt-10 pb-6"
            v-else-if="tickets && tickets.length > 0"
            v-for="ticket in filteredTickets().reverse()"
            :key="ticket.id"
            elevation="4"
        >
          <!-- Ticket card header -->
          <v-row>
            <v-icon class="ticket-icon mr-5" large size="80px"> mdi-download</v-icon>
            <v-sheet elevation="0" color="transparent" class="d-flex flex-column justify-center">
              <span class="ticket-name font-weight-bold text-h4 pb-2">{{ ticket.name }}</span>
              <span class="ticket-date text-h6 font-weight-medium"
                    v-if="ticket.valid_from_date && ticket.valid_from_time">
                {{ ticket.valid_from_time }} {{ ticket.valid_from_date }}
              </span>
            </v-sheet>

            <v-divider color="black" opacity="0.7" class="my-4" />
          </v-row>

          <!-- Ticket card body -->
          <v-row class="justify-space-between align-center">
            <v-select
                :items="['Jan', 'Anna', 'Piotr']"
                label="Przypisz do osoby (Opcjonalnie)"
                variant="outlined"
                multiple
                bg-color="background"
                max-width="600px"
                min-width="200px"
                rounded="lg"
            />

            <!-- Button to download the ticket -->
            <AppButton
                variant="primary"
                width="200px"
                class="mb-5"
                @click="() => downloadFile(ticket.file)"
                height="height-auto"
                font-size="font-auto"
            >
              <v-icon>mdi-download</v-icon>
              <span class="pl-1">Pobierz bilet</span>
            </AppButton>
          </v-row>
        </v-card>
      </v-col>
    </template>
  </Section>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.ticket-icon {
  color: $text-color;
}

.ticket-card {
  background-color: $background-secondary;
}

.ticket-date {
  color: $primary-color;
}

.ticket-name {
  color: $text-color;
}

.empty-tickets {
  background-color: $background-secondary;
}

.add-link {
  color: $primary-color;
}

</style>
