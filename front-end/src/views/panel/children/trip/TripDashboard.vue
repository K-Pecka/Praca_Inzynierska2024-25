<script lang="ts" setup>
import {images} from "@/data";
import {shallowRef} from 'vue';
import {
  YourPlan, YourTrip, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm, PlanForm, BudgetForm
} from "@/views/panel";
import {useMockupStore} from "@/mockup/useMockupStore";

const {getUserInitials} = useMockupStore();

const userInitials = getUserInitials();

const items = [
    { title: 'Ustawienia konta', to: "AccountSettings" },
    { title: 'Wybór roli', to: "panel" },
  ]

const side_nav_items = [
  {
    title: 'Panel',
    page: ExpenseTracker,
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
    page: TripEditForm,
    icon: 'mdi-cog-outline',
    children: [
      {
        title: 'Edycja wycieczki',
        page: TripEditForm,
      }
    ]
  },
]

const downloadTicket = (url: any) => {
  const link = document.createElement('a');
  link.href = url;
  link.download = ''; // optionally force download
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

const handleClick = async (navigate: Function) => {
  try {
    await navigate();
  } catch (error) {
    console.error("Navigation failed", error);
  }
};

const currentPage = shallowRef(ExpenseTracker);

const loadPage = (page: any) => {
  currentPage.value = page;
};
</script>

<template>
  <v-container fluid>
    <v-app-bar flat style="border-bottom: 2px solid rgb(var(--v-theme-primary));">
      <router-link to="/" class="ml-3" style="text-decoration: none;">
        <v-img class="ml-3" aspect-ratio="16/9" width="10%" min-width="120px" cover :src="images.logo.img" />
      </router-link>
      <template v-slot:append>

        <v-menu>
          <template v-slot:activator="{ props }">
            <div v-bind="props" class="account-menu-trigger">
              <v-avatar color="red">
                <span class="text-h5">{{ userInitials }}</span>
              </v-avatar>
              <span class="ml-2 account-text">Moje Konto</span>
              <v-icon class="ml-1">mdi-chevron-down</v-icon>
            </div>
          </template>

          <v-list>
            <router-link
              v-for="(item, i) in items"
              :key="i"
              :to="{ name: item.to}"
              custom
              v-slot="{ navigate }"
            >
              <v-list-item @click="handleClick(navigate)">
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </router-link>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>
   <v-navigation-drawer>
  <v-list>
    <template v-for="item in side_nav_items">
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
          :active="currentPage === subItem.page"
          @click="downloadTicket('https://api.plannder.com/media/tickets/XZD.jpeg')"
          slim
          class="pl-6"
        />
      </v-list-group>

      <v-list-item
        v-else
        :title="item.title"
        :prepend-icon="item.icon"
        :active="currentPage === item.page"
        @click="loadPage(item.page)"
        slim
        class="pl-3"
      />
    </template>

    <v-divider />

  </v-list>

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
    <v-col cols="12">
      <component :is="currentPage" class="component-section" />
    </v-col>
  </v-container>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.component-section {
  bottom: 0;
  right: 0;
  z-index: 1005;
  overflow-y: auto;
  transform: translateY(0px);
  position: fixed;
  height: calc(100% - $header-size);
  width: calc(100% - 256px);

  @media
  (max-width: 1279px) {
    width: 100%;
  }
}
.account-menu-trigger {
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.account-menu-trigger:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.account-text {
  position: relative;
}

.account-text::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: -2px;
  left: 0;
  background-color: #2F27CE;
  transition: width 0.3s ease;
}

.account-menu-trigger:hover .account-text::after {
  width: 100%;
}

.account-menu-trigger:hover .account-text {
  color: #2F27CE;
}

.account-menu-trigger:hover .v-icon {
  color: #2F27CE;
  transform: translateY(1px);
}
</style>
