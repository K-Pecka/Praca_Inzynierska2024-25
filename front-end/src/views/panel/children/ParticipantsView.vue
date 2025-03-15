<script setup lang="ts">
import {ref, computed} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import AppButton from "@/components/budget/AppButton.vue";
import ParticipantList from "@/components/trip/ParticipantList.vue";
import {Participant} from "@/type";
import {useTripStore} from "@/stores";

const participants = ref<Participant[]>([
  // {
  //   id: "p1",
  //   name: "Mateusz Wiśniewski",
  //   email: "s24893@pjwstk.edu.pl",
  //   role: "przeglądanie",
  // },
  // {
  //   id: "p2",
  //   name: "Mateusz Wiśniewski",
  //   email: "s24893@pjwstk.edu.pl",
  //   role: "przeglądanie",
  // },
  // {
  //   id: "p3",
  //   name: "Mateusz Wiśniewski",
  //   email: "s24893@pjwstk.edu.pl",
  //   role: "przeglądanie",
  // },
]);

const maxParticipants = 5;
const countLabel = computed(() => `${participants.value.length}/${maxParticipants}`);

const inviteEmail = ref("");

function inviteParticipant() {
  const {invateUserMutation} = useTripStore();
  invateUserMutation.mutateAsync(inviteEmail.value);
}

const route = useRoute();
</script>

<template>
  <div class="page-container">
    <Section>
      <template #title>
        <div class="top-bar">
          <div class="invite-wrapper">
            <div class="invite-container">
              <input
                  v-model="inviteEmail"
                  class="invite-input"
                  placeholder="Podaj email uczestnika"
              />
              <AppButton variant="primary" @click="inviteParticipant">
                Zaproś
              </AppButton>
            </div>
            <div class="count-label">
              {{ countLabel }}
            </div>
          </div>
        </div>
      </template>

      <template #content>
        <ParticipantList
            :participants="participants"
        />
      </template>
    </Section>
  </div>
</template>

<style scoped lang="scss">
.page-container {
  max-width: 88rem;
  margin: 0 auto;
  padding-top: 0;
}

.top-bar {
  display: flex;
  justify-content: center;
  width: 100%;
}

.invite-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.invite-container {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 1rem;
}

.invite-input {
  flex-grow: 1;
  padding: 0.75rem 1rem;
  border-radius: 20px;
  background-color: rgb(var(--v-theme-background));
  border: 1px solid rgba(0, 0, 0, 0.2);
  font-size: 1rem;
}

.count-label {
  font-size: 2rem;
  font-weight: bold;
  text-align: left;
  margin-top: 0.5rem;
}
</style>
