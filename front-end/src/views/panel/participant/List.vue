<script setup lang="ts">
import {computed, ref} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import ParticipantList from "@/components/trip/module/participant/ParticipantList.vue";
import ParticipantsCounter from "@/components/trip/module/participant/ParticipantsCounter.vue";
import ParticipantAddForm from "@/components/trip/module/participant/ParticipantAddForm.vue";
import {useTripStore, useNotificationStore,useAuthStore, useUtilsStore} from "@/stores";
import HeaderSection from "@/components/shared/HeaderSection.vue";
const {getTripId} = useUtilsStore()
const {setErrorCurrentMessage} = useNotificationStore();
const route = useRoute();
const tripId = Number(route.params.tripId);

const {userData,isGuide} = useAuthStore();
const {isOwner} = userData;
const {trip:tripStore,participant} = useTripStore();
const {getTripDetails} = tripStore;

const {removeParticipant, addParticipant} = participant
const {trip} = getTripDetails();

import {useMembersStore} from "@/stores/trip/useMembersStore"
const {setData} = useMembersStore();

const members = computed(() => {
  if (trip.value !== undefined) {
    setData(trip.value);
  }
  return useMembersStore().members.filter(e => !e.is_owner) || [];
});


const maxParticipants = 5;

const showForm = ref(false);

function inviteParticipant(participant: { email: string }) {
  if (members.value.length == maxParticipants && !isGuide()) {
    setErrorCurrentMessage("Osiągnięto limit");
    showForm.value=false;
    return;
  }
  addParticipant(Number(tripId), participant);
  showForm.value=false
}

const toggleForm = () => {
  showForm.value = !showForm.value;
};

import {useSafeDelete} from "@/composables/useSafeDelete";
const {confirmAndRun} = useSafeDelete();
const removeParticipantById = (id: number) => {
  confirmAndRun(() => {
    removeParticipant(Number(getTripId()), id);
  }, {
    title: "Potwierdź usunięcie uczestnika",
    message: "Czy na pewno chcesz usunąć tego uczestnika? Tego działania nie można cofnąć.",
    wordToConfirm: "USUŃ"
  });
};
</script>

<template>
    <Section>
      <template #title>
        <HeaderSection
            subtitle="Zarządzaj uczestnikami"
            :button="isOwner(trip?.creator?.id ?? 0) && maxParticipants != members.length || isGuide()"
            button-text="Dodaj"
            :button-action="toggleForm"
        />
      </template>

    <template #content>
      <v-container fluid>
        <v-row>
          <v-col>
            <ParticipantsCounter
                v-if="!isGuide()"
                :current="members.length"
                :max="maxParticipants"
                title="Uczestnicy"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <ParticipantAddForm
                v-model:dialog="showForm"
                title="Dodaj uczestnika"
                @cancel="showForm = false"
                @submitForm="inviteParticipant"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-card class="background-secondary" rounded="lg">
              <v-card-text class="pa-6">
                <span class="text-h5 font-weight-bold">
                  Dodani uczestnicy
                </span>

                <ParticipantList
                    v-if="members.length > 0"
                    :participants="members"
                    @remove="removeParticipantById"
                />
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </Section>
</template>
