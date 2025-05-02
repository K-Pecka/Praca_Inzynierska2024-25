<script lang="ts" setup>
import {useRouter} from "vue-router";

import {onMounted, shallowRef} from "vue";

const router = useRouter();

const side_nav_items = shallowRef([
  {
    title: 'Panel',
    page: {name: 'tripDashboard'},
    icon: 'mdi-home-outline'
  },
  {
    title: 'Plany',
    icon: 'mdi-note-text-outline',
    children: [
      {title: 'Utworzone', page: {name: 'tripPlans'}},
      {title: 'Dodaj', page: {name: 'createPlan'}},
    ]
  },
  {
    title: 'Bilety',
    page: {name: 'yourTickets'},
    icon: 'mdi-ticket-confirmation-outline'
  },
  {
    title: 'Budżet',
    icon: 'mdi-currency-usd',
    children: [
      {title: 'Pokaż', page: {name: 'ExpenseTracker'}},
      {title: 'Zmień budżet', page: {name: 'editBudget'}},
    ]
  },
  {
    title: 'Uczestnicy',
    page: {name: 'tripParticipants'},
    icon: 'mdi-account-multiple-outline'
  },
  {
    title: 'Ustawienia',
    icon: 'mdi-cog-outline',
    children: [
      {
        title: 'Edycja wycieczki',
        page: {name: 'editTrip'},
      }
    ]
  },
]);

onMounted(() => {
  router.push({name: 'tripDashboard'})
})
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
              :active="router.currentRoute.value.name === subItem.page.name"
              @click="router.push(subItem.page)"
              slim
              class="pl-6"
          />
        </v-list-group>

        <!-- Pages without children -->
        <v-list-item
            v-else
            :title="item.title"
            :prepend-icon="item.icon"
            :active="router.currentRoute.value.name === item.page.name"
            @click="router.push(item.page)"
            slim
            class="pl-3"
        />
      </template>
      <v-divider/>
    </v-list>

    <!-- Return button -->
    <v-list-item
        title="Powrót"
        link
        prepend-icon="mdi-arrow-left"
        slim
        class="pl-3"
        @click="router.back()"
    />
  </v-navigation-drawer>
</template>

<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

</style>

