<script setup lang="ts">
import { User } from "@/types";
import AppButton from "../../../AppButton.vue";

const props = defineProps<{
  user: User;
}>();

const emit = defineEmits(["remove"]);

function handleRemoveClick() {
  console.log("handleRemoveClick", props.user.userId);
  emit("remove", props.user.userId);
}

const tags = [
  {
    name: "Oczekujący",
    style: "bg-orange-darken-2",
    condition: props.user.is_guest === true,
  },
  {
    name: "Potwierdzony",
    style: "bg-green",
    condition: props.user.is_guest === false,
  },
];
import {useAuthStore,useTripStore} from "@/stores"
const {userData} = useAuthStore();
const {isOwner} = userData;

const {trip:tripStore} = useTripStore();
const {getTripDetails} = tripStore;
const {trip} = getTripDetails();
const hasPermissionToDelete = () => {
  if(isOwner(trip.value?.creator?.id ?? 0))
  {
    handleRemoveClick()
  }
};
</script>

<template>
  <v-col cols="12">
    <v-row>
      <v-card
        :class="{ 'participant-item--noactive': user.is_guest }"
        class="w-100"
        rounded="lg"
        elevation="0"
      >
        <v-card-text>
          <v-row align="center" no-gutters>
            <v-col>
              <v-row no-gutters align="center">
                <v-icon size="48" class="color-primary"
                  >mdi-account-outline</v-icon
                >
                <v-col>
                  <span class="text-h6 font-weight-bold">{{ user.name }}</span>
                  <v-row align="center" no-gutters>
                    <v-icon size="18" color="#555" class="mr-1"
                      >mdi-email-outline</v-icon
                    >
                    <span>{{ user.email }}</span>
                  </v-row>
                </v-col>
              </v-row>
            </v-col>
            <v-col class="tags-row text-center" no-gutters>
              <v-col
                v-for="tag in tags.filter((tag) => tag.condition)"
                :key="tag.name"
                cols="auto"
              >
                <v-chip
                  variant="outlined"
                  size="medium"
                  class="status-chip text-subtitle-1 text-center justify-center px-3"
                  :class="tag.style"
                  style="font-weight: 600"
                >
                  {{ tag.name }}
                </v-chip>
              </v-col>
            </v-col>
            <v-col class="text-end">
              <AppButton
                color="red"
                font-auto
                max-width="190px"
                text="Usuń uczestnika"
                @click="hasPermissionToDelete"
                :disabled="!isOwner(trip?.creator?.id ?? 0)"
              />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-row>
  </v-col>
</template>

<style scoped lang="scss">
.participant-item--noactive {
  background-color: rgba(var(--v-theme-background), 0.6);
}
</style>
