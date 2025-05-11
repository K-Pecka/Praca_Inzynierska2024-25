<script setup lang="ts">
  import {usePagePanelStore} from "@/stores/ui/usePagePanelStore";
  import { useDisplay } from "vuetify";
  import {computed} from "vue";
  import {RoleSelection} from "@/types";

  const pagePanelStore = usePagePanelStore();
  const getRoleSelection = computed<RoleSelection>(() => pagePanelStore.getRoleSelection);
  const { smAndDown } = useDisplay();
</script>

<template>
  <v-col cols="12" md="8" xl="8" class="role-selection mx-auto">
    <v-row class="flex-column">
      <span class="text-center font-weight-bold pb-4 text-h4">{{ getRoleSelection.title }}</span>
      <span class="text-center text-h5">{{ getRoleSelection.subtitle }}</span>
    </v-row>

    <v-row justify="space-between" class="mt-6">
      <v-col
        v-for="role in getRoleSelection.roles"
        :key="role.title"
        class="py-12"
        :class="{ 'px-12': !smAndDown }"
        cols="12"
        lg="6"
        md="6"
      >
        <router-link :to="role.path" class="text-decoration-none">
          <v-card
              class="role-card d-flex flex-column align-center"
              elevation="4"
              height="auto"
              width="auto"
          >
            <v-img
              :src="role.image.img"
              :alt="role.image.alt"
              contain
              width="30%"
              min-width="150"
              class="mb-4"
            />
            <div class="text-center pb-6 w-auto h-auto" :class="{ 'px-2': smAndDown }">
              <div class="text-h4 font-weight-medium role-title pb-3">{{ role.title }}</div>
              <div class="text-body-1 text-grey-darken-1">{{ role.description }}</div>
            </div>
          </v-card>
        </router-link>
      </v-col>
    </v-row>
  </v-col>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.role-card {
  padding-block: 1rem;
  background-color: $background-secondary;
}

.text-h4 {
  color: rgb($primary-color);
}

.choose-profile-button {
  background-color: $background-secondary;
}

.role-title {
  color: rgb($primary-color);
}


</style>