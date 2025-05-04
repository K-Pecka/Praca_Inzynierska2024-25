<script setup lang="ts">
import {ref, watchEffect} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";

import {useTripStore} from "@/stores/trip/useTripStore";


import TicketForm from "@/components/trip/module/ticket/TicketForm.vue";
import AppButton from "@/components/budget/AppButton.vue";
import {useUtilsStore} from "@/stores";
import HeaderSection from "@/components/common/HeaderSection.vue";
import {createTicket,fetchUserById} from "@/api"
import axios from "axios";
const {combineDateAndTime} = useUtilsStore();
const route = useRoute();
const tripId = route.params.tripId as string;
const {data: tripData} = useTripStore().getTripDetails(Number(tripId));
const {data: tickets, isLoading} = useTripStore().getTickets(tripId);
const getUserById =async (id:number)=>{
  const user = await fetchUserById(id);
  //console.log(user)
  return {
    name: `${user.first_name} ${user.last_name}`,
    userId: id
  };
}
const members = ref<{ name: string; userId: number }[]>([]);

watchEffect(async () => {
  const membersRaw = tripData.value?.members ?? [];
  const pendingRaw = tripData.value?.pending_members ?? [];

  const confirmed = await Promise.all(
    membersRaw.map(async (entry) => {
      const id =  entry;
      const user = await getUserById(id);
      return { ...user, is_guest: false };
    })
  );

  const pending = await Promise.all(
    pendingRaw.map(async (entry) => {
      const id = typeof entry === 'object' && entry !== null ? entry.id : entry;
      const user = await getUserById(id);
      return { ...user, is_guest: true };
    })
  );
  const userMap = new Map<number, typeof confirmed[0]>();
  
  for (const user of [...pending, ...confirmed]) {
    userMap.set(user.userId, user);
  }

  members.value = Array.from(userMap.values());
});
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
    await createTicket(formData,{ tripId:tripId });
    showForm.value = false;
  } catch (error) {
    //console.error("Błąd podczas tworzenia biletu:", error);
  }
}

const downloadItem = async ( url: string )=> {
  //console.log(url)
      const response = await axios.get(url, { responseType: "blob" });
      const blob = new Blob([response.data], { type: "application/jpeg" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "Prosze pobierz się.jpeg";
      link.click();
      URL.revokeObjectURL(link.href);
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
            :members="members"
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
            class="background-secondary rounded-xl my-5"
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
                  :items="members"
                  :disabled="members.length === 0"
                  label="Przypisz do osoby (Opcjonalnie)"
                  variant="outlined"
                  multiple
                  item-title="name"
                  item-value="userId"
                  density="compact"
                  bg-color="background"
                  max-width="600px"
                  min-width="200px"
                  rounded="lg"
              />

              <!-- Button to download the ticket -->
              <AppButton
                  variant="primary"
                  @click="() => downloadItem(ticket.file)"
                  height-auto
                  font-auto
                  text="Pobierz bilet"
                  stretch
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
