<script setup lang="ts">
  import { images } from "@/data";
  import { useMockupStore } from "@/mockup/useMockupStore";
  import { usePanelStore} from "@/stores/panel/usePanelStore";

  const panelStore = usePanelStore();

  const { getUserInitials } = useMockupStore();
  const userInitials = getUserInitials();

</script>

<template>
  <v-container min-height="150px">
    <v-app-bar class="header" flat>

      <!-- Logo -->
      <router-link to="/" class="ml-3">
        <v-img class="ml-3" aspect-ratio="16/9" width="10%" min-width="120px" cover :src="images.logo.img" />
      </router-link>

      <!-- Nav -->
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

          <!-- Dropdown Menu -->
          <v-list>
            <router-link
              v-for="(item, i) in panelStore.items"
              :key="i"
              :to="{ name: item.to}"
              custom
              v-slot="{ navigate }"
            >
              <v-list-item @click="panelStore.handleClick(navigate)">
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </router-link>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>
  </v-container>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.header {
  border-bottom: $panel-header-border-bottom;
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
