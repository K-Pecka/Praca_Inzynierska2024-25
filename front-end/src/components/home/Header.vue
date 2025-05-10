<script lang="ts" setup>
  import { computed } from "vue"
  import { useRouter } from "vue-router"

  import { useDisplay } from 'vuetify'

  import { images } from '@/data'
  import { usePageHomeStore } from '@/stores'
  import { usePanelStore } from '@/stores/panel/usePanelStore'

  const pageHomeStore = usePageHomeStore()
  const panelStore = usePanelStore()
  const router = useRouter()

  interface NavItem {
    title: string
    to: string | { name: string }
    show: boolean | (() => boolean)
  }

  const items = <NavItem[]>([
    { title: "Oferta", to: { name: "pricingSection" }, show: true },
    { title: "O nas", to: { name: "aboutUs" }, show: true },
    { title: "Kontakt", to: { name: "contactUs" }, show: true },
    { title: "Zaloguj się", to: { name: "logIn" }, show: () => !pageHomeStore.isLoggedIn },
    { title: "Zarejestruj się", to: { name: "register" }, show: () => !pageHomeStore.isLoggedIn },
    { title: "Wyloguj się", to: { name: "logOut" }, show: () => pageHomeStore.isLoggedIn },
    { title: "Panel", to: { name: "roleSelection" }, show: () => pageHomeStore.isLoggedIn },
  ]);

  const visibleItems = computed(() =>
    items.filter(item =>
      typeof item.show === 'function' ? item.show() : item.show
    )
  );

  const { smAndDown } = useDisplay()
</script>

<template>
  <v-app-bar :height="100" class="header mt-5 bg-header" absolute>
    <!-- Logo -->
    <template v-slot:prepend>
      <router-link to="/" class="d-flex items-center pl-5">
        <v-img
          aspect-ratio="16/9"
          :src="images.logo.img"
          :min-width="150"
          :max-width="250"
        />
      </router-link>
    </template>

    <!-- Desktop nav -->
    <template v-slot:append>
      <div class="pr-5" v-if="!smAndDown">
        <v-btn
          v-for="(item, i) in visibleItems"
          :key="i"
          :to="item.to"
          variant="text"
          class="px-3 rounded-lg"
          :class="[item.title === 'Panel' || item.title === 'Zarejestruj się' ? 'panel-button gradient-bg' : '']"
        >
          {{ item.title }}
        </v-btn>
      </div>

      <!-- Mobile nav -->
      <v-menu v-else>
        <template v-slot:activator="{ props }">
          <v-app-bar-nav-icon v-bind="props" />
        </template>
        <v-list>
          <v-list-item
            v-for="(item, i) in visibleItems"
            :key="i"
            @click="panelStore.handleClick(() => router.push(item.to))"
            link
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-app-bar>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.header-container {
  min-height: 200px;
}

.header {
  border: $main-header-border;
  border-radius: $main-header-border-radius;
  width: 80% !important;
  left: 10% !important;

}

.panel-button {
  background-color: rgb($primary-color);
  color: white;
}
</style>