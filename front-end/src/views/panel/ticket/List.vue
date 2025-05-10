<script setup lang="ts">
import {computed, ref, watchEffect} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";

import {useTripStore} from "@/stores/trip/useTripStore";


import TicketForm from "@/components/trip/module/ticket/TicketForm.vue";
import AppButton from "@/components/AppButton.vue";
import {useUtilsStore} from "@/stores";
import HeaderSection from "@/components/common/HeaderSection.vue";
import {createTicket, fetchUserById} from "@/api"
import axios from "axios";

const {combineDateAndTime, getTripId} = useUtilsStore();
const {trip: tripStore} = useTripStore();
const {getTripDetails} = tripStore;
const {trip} = getTripDetails();
const {data: tickets, isLoading} = useTripStore().getTickets(String(getTripId()));


import {useMembersStore} from "@/stores/trip/useMembersStore"

const {members: membersStore} = useMembersStore();
const members = computed(() => membersStore)

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
  formData.append("trip", String(getTripId()));
  formData.append("valid_from_date", newTicketData.date);
  formData.append("valid_from_time", newTicketData.time);
  formData.append("file", newTicketData.file);
  try {
    await createTicket(formData, {tripId: String(getTripId())});
    showForm.value = false;
  } catch (error) {
    //console.error("Błąd podczas tworzenia biletu:", error);
  }
}

const downloadItem = async (url: string) => {
  ////console.log(url)
  const response = await axios.get(url, {responseType: "blob"});
  const blob = new Blob([response.data], {type: "application/jpeg"});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "Prosze pobierz się.jpeg";
  link.click();
  URL.revokeObjectURL(link.href);
}

const filteredTickets = () => {
  return (
      tickets.value?.filter((ticket) => ticket.trip === Number(getTripId())) ?? []
  );
};

const toggleForm = () => {
  showForm.value = !showForm.value;
};

</script>

<template>
  <Section>
    <template #title>
      <HeaderSection
          subtitle="Bilety"
          button
          button-text="Dodaj Bilet"
          :button-action="toggleForm"
      />
    </template>

    <template #content>

      <!-- Ticket create form -->
      <v-col cols="12" class="pa-0" v-if="showForm">
        <TicketForm
            :members="members"
            @submitTicket="handleAddTicket"
            @cancelForm="showForm = false"
            class="form-container"
        />
      </v-col>

      <!-- Ticket cards -->
      <v-col cols="12">
        <v-row>
          <!-- Empty state when no tickets are present -->
          <v-card
              v-if="!isLoading && tickets && tickets.length === 0"
              class="background-secondary"
          >
            <v-card-text>
              <v-row>
                <v-col>
                  <v-row justify="center" no-gutters>
                    <v-icon size="48" color="black"
                    >mdi-ticket-confirmation-outline
                    </v-icon>
                  </v-row>
                </v-col>
                <v-col>
                  <v-row justify="center" no-gutters>
                    <p>Brak dodanych biletów</p>
                    <a class="color-primary" @click="showForm = true">
                      Dodaj pierwszy bilet
                    </a>
                  </v-row>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>


          <!-- Ticket -->
          <v-card
              class="background-secondary rounded-lg mb-6 w-100 pa-4"
              v-else-if="tickets && tickets.length > 0"
              v-for="ticket in filteredTickets().reverse()"
              :key="ticket.id"
              elevation="4"
          >
            <v-card-text>


              <!-- Icon with text -->
              <v-row justify="center">
                <v-col cols="12" xs="12" sm="8" md="5" lg="5">
                  <v-row align="center" no-gutters>
                    <v-icon class="color-text" large size="70px"> mdi-download</v-icon>
                    <v-row no-gutters class="flex-column justify-center pl-4">
                      <span class="color-text font-weight-bold text-h5">{{ ticket.name }}</span>
                      <span class="color-primary text-h6 font-weight-medium"
                            v-if="ticket.valid_from_date && ticket.valid_from_time">
                        {{ ticket.valid_from_time }} {{ ticket.valid_from_date }}
                      </span>
                    </v-row>
                  </v-row>
                </v-col>


                <!-- Select -->
                <v-col cols="12" xs="12" sm="8" md="4" lg="4">
                  <v-row align="center" justify="center" class="h-100" no-gutters>
                    <v-select
                        :items="members"
                        :disabled="members.length === 0"
                        label="Przypisz do osoby (Opcjonalnie)"
                        variant="outlined"
                        multiple
                        item-title="name"
                        item-value="userId"
                        density="compact"
                        bg-color="background"
                        rounded="lg"
                    />
                  </v-row>
                </v-col>


                <!-- Buttons -->
                <v-col cols="12" xs="12" sm="8" md="3" lg="3">
                  <v-row justify="end" align="center" class="h-100" no-gutters>
                    <v-col
                        cols="6"
                        sm="6"
                        md="12"
                        lg="12"
                        :class="$vuetify.display.smAndDown ? 'text-start' : 'text-end'">
                      <AppButton
                          color="primary-outline"
                          @click="() => downloadItem(ticket.file)"
                          font-auto
                          max-width="190px"
                          text="Pobierz bilet"
                      />
                    </v-col>
                    <v-col cols="6" sm="6" md="12" lg="12" class="text-end">
                      <AppButton
                          color="red"
                          @click="() => downloadItem(ticket.file)"
                          font-auto
                          max-width="190px"
                          text="Usuń bilet"
                      />
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-row>
      </v-col>
    </template>
  </Section>
</template>

<style lang="scss">
.v-select .v-input__details {
  position: absolute;
}
</style>
