<script setup lang="ts">
import { TicketData, User } from "@/types";
import { useSafeDelete } from "@/composables/useSafeDelete";
import axios from "axios";
import { onMounted, ref, watch, watchEffect } from "vue";
import { AppButton } from "@/components";
import { useAuthStore, useTripStore, useUtilsStore } from "@/stores";

// Stores
const { ticket: ticketStore } = useTripStore();
const { deleteTicket,updateMembers } = ticketStore;
const { userData } = useAuthStore();
const { isOwner } = userData;
const { getTripId } = useUtilsStore();
const { confirmAndRun } = useSafeDelete();

// Props
const { ticket, members, creatorId, refetchTickets } = defineProps<{
  ticket: TicketData;
  members: User[];
  creatorId: number;
  refetchTickets: () => any;
}>();

// Permissions
const hasPermissionToDelete = () => isOwner(creatorId);

// Delete logic
const handleDelete = (trip: number) => {
  confirmAndRun(() => {
    handleDeleteTicket(trip);
  }, {
    title: "Potwierdź usunięcie biletu",
    message: "Czy na pewno chcesz usunąć ten bilet? Tego działania nie można cofnąć.",
    wordToConfirm: "USUŃ"
  });
};

const handleDeleteTicket = (ticketId: number) => {
  deleteTicket.mutate({
    tripId: String(getTripId()),
    ticketId: String(ticketId),
  });
};

// Download logic
const downloadItem = async (url: string) => {
  const response = await axios.get(url, { responseType: "blob" });
  const blob = new Blob([response.data], { type: response.headers['content-type'] });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "Bilet.jpeg";
  link.click();
  URL.revokeObjectURL(link.href);
};

const selectedMembers = ref<User[]>([]);

watchEffect(() => {
  if (members.length && ticket.profiles.length) {
    selectedMembers.value = ticket.profiles
      .map(profileId => members.find(member => member.userId === profileId))
      .filter(Boolean) as User[];
  }
});
let initialized = false;
watch(selectedMembers,(newSelected,oldSelected)=>{
    if (!initialized) {
        initialized = true;
        return;
    }
    if (newSelected) {
        updateMembers.mutate({
            newMembers: newSelected.map(el => el.userId),
            param: {
                tripId: String(getTripId()),
                ticketId: String(ticket.id),
            }
        });
    }
})
</script>


<template>
  <v-card class="background-secondary rounded-lg mb-6 w-100 pa-4" elevation="4">
    <v-card-text>
      <v-row justify="center">
        <!-- Ikona i informacje -->
        <v-col cols="12" xs="12" sm="8" md="5" lg="5">
          <v-row class="h-100" align="center" justify="center" no-gutters>
            <v-icon class="color-text" large size="70px" color="primary">
              mdi-ticket
            </v-icon>
            <v-row no-gutters class="flex-column justify-center pl-4">
              <span class="color-text font-weight-bold text-h5">{{ ticket.name }}</span>
              <span
                class="color-primary text-h6 font-weight-medium"
                v-if="ticket.valid_from_date && ticket.valid_from_time"
              >
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
              v-model="selectedMembers"
              :disabled="members.length === 0"
              label="Przypisz do osoby (Opcjonalnie)"
              variant="outlined"
              multiple
              item-title="email"
              item-value="userId"
              density="compact"
              bg-color="background"
              rounded="lg"
              return-object
              :menu-props="{ closeOnContentClick: false }"
              chips
            />
          </v-row>
        </v-col>

        <!-- Przyciski -->
        <v-col cols="12" xs="12" sm="8" md="3" lg="3">
          <v-row justify="end" align="center" class="h-100" no-gutters>
            <v-col
              cols="6"
              sm="6"
              md="12"
              lg="12"
              :class="$vuetify.display.smAndDown ? 'text-start' : 'text-end'"
            >
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
                @click="hasPermissionToDelete() ? handleDelete(ticket.id) : () => {}"
                :disabled="!hasPermissionToDelete()"
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
</template>


<style scoped lang="scss">
.ticket-card {
  min-height: 300px;
}
</style>
