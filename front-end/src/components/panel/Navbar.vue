<script lang="ts" setup>
  import { usePanelStore } from "@/stores/panel/usePanelStore";
  import {
    BudgetForm,
    ExpenseTracker,
    ParticipantsView,
    PlanForm,
    TicketsView,
    TripDashboard,
    TripEditForm,
    YourPlan
  } from "@/views";

  import { shallowRef } from "vue";

  const side_nav_items = shallowRef([
    {
      title: 'Panel',
      page: TripDashboard,
      icon: 'mdi-home-outline'
    },
    {
      title: 'Plany',
      icon: 'mdi-note-text-outline',
      children: [
        { title: 'Utworzone', page: YourPlan },
        { title: 'Dodaj', page: PlanForm },
      ]
    },
    {
      title: 'Bilety',
      page: TicketsView,
      icon: 'mdi-ticket-confirmation-outline'
    },
    {
      title: 'Budżet',
      icon: 'mdi-currency-usd',
      children: [
        { title: 'Pokaż', page: ExpenseTracker },
        { title: 'Zmień budżet', page: BudgetForm },
      ]
    },
    {
      title: 'Uczestnicy',
      page: ParticipantsView,
      icon: 'mdi-account-multiple-outline'
    },
    {
      title: 'Ustawienia',
      icon: 'mdi-cog-outline',
      children: [
        {
          title: 'Edycja wycieczki',
          page: TripEditForm,
        }
      ]
    },
  ]);

  const panelStore = usePanelStore();
  panelStore.loadPage(TripDashboard)
</script>

<template>
  <v-navigation-drawer>
    <!-- Navigation Drawer -->
    <v-list>
      <template v-for="item in side_nav_items">
        <!-- Pages with children -->
        <v-list-group
          v-if="item.children"
          prepend-icon="mdi-chevron-down"
        >
          <template #activator="{ props }">
            <v-list-item
              v-bind="props"
              :title="item.title"
              :prepend-icon="item.icon"
              slim
              class="pl-3"
            />
          </template>

          <v-list-item
            v-for="subItem in item.children"
            :key="subItem.title"
            :title="subItem.title"
            :active="panelStore.currentPage === subItem.page"
            @click="panelStore.loadPage(subItem.page)"
            slim
            class="pl-6"
          />
        </v-list-group>

        <!-- Pages without children -->
        <v-list-item
          v-else
          :title="item.title"
          :prepend-icon="item.icon"
          :active="panelStore.currentPage === item.page"
          @click="panelStore.loadPage(item.page)"
          slim
          class="pl-3"
        />
      </template>
      <v-divider />
    </v-list>

    <!-- Return button -->
    <router-link :to="{ name: 'yourTrip' }" style="color: black;">
      <v-list-item
        title="Powrót"
        link
        prepend-icon="mdi-arrow-left"
        slim
        class="pl-3"
      />
    </router-link>
  </v-navigation-drawer>
</template>

<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

</style>

