<script setup lang="ts">
import {computed, ref} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import ParticipantList from "@/components/trip/module/participant/ParticipantList.vue";
import ParticipantsCounter from "@/components/trip/module/participant/ParticipantsCounter.vue";
import ParticipantAddForm from "@/components/trip/module/participant/ParticipantAddForm.vue";
import {useTripStore, useNotificationStore,useAuthStore} from "@/stores";
import HeaderSection from "@/components/common/HeaderSection.vue";

const {setErrorCurrentMessage} = useNotificationStore();
const route = useRoute();
const tripId = Number(route.params.tripId);

const {userData} = useAuthStore();
const {isOwner} = userData;
const {trip:tripStore} = useTripStore();
const {getTripDetails} = tripStore;
const {trip} = getTripDetails();
const {removeParticipant, addParticipant,} = useTripStore();

import {useMembersStore} from "@/stores/trip/useMembersStore"

const {members: membersStore} = useMembersStore();
const members = computed(() => membersStore)


const maxParticipants = 5;

const showForm = ref(false);

function inviteParticipant(participant: { name: string; email: string }) {
  if (members.value.length == maxParticipants) {
    setErrorCurrentMessage("Osiągnięto limit");
    return;
  }
  addParticipant(Number(tripId), participant);
}

function removeParticipantById(id: number) {
  removeParticipant(Number(tripId), id);
}

const toggleForm = () => {
  showForm.value = !showForm.value;
};
</script>

<template>
    <Section>
      <template #title>
        <HeaderSection
            subtitle="Zarządzaj uczestnikami"
            :button="isOwner(trip?.creator?.id || 0)"
            button-text="Dodaj"
            :button-action="toggleForm"
        />
      </template>

    <template #content>
      <v-container fluid>
        <v-row>
          <v-col>
            <ParticipantsCounter
                :current="members.length"
                :max="maxParticipants"
                title="Uczestnicy"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <ParticipantAddForm
                v-if="showForm"
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
