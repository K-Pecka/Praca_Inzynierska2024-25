<script lang="ts" setup>
import Navbar from "@/components/main/Navbar.vue";
import Footer from "@/components/main/Footer.vue";

const SiteName = import.meta.env.VITE_APP_SITE_NAME || "Plannder";

const navLinksBase = [
  { label: "Oferta", href: "/", className: ["navbar__link--base"] },
  { label: "O nas", href: "/", className: ["navbar__link--base"] },
  { label: "Kontakt", href: "/", className: ["navbar__link--base"] },
];
const user = localStorage.getItem("user") || false;
const navLinks = [
  ...navLinksBase,
  ...(user
    ? [{ label: "Panel", href: "/", active: true }]
    : [
        { label: "Zaloguj się", href: "/logIn" },
        { label: "Zarejestruj się", href: "/register", active: true },
      ]),
];
const footerData = {
  links: [...navLinksBase, { label: "Panel", href: "/" }],
  footerText: `© 2025 Plannder Wszystkie prawa zastrzeżone `,
  subSection: `ostatnia modyfikacja: ${new Date().toLocaleDateString()}`,
};
</script>

<template>
  <v-app>
    <v-container fluid class="full-width-container">
      <v-row class="sticky-top fixed-center">
        <v-col cols="12" md="10" offset-md="1">
          <Navbar :links="navLinks">
            <template #logo>
              <img src="@/assets/vue.svg" alt="App Logo" />
            </template>
          </Navbar>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="10" lg="8" offset-lg="2" offset-md="1">
          <main>
            <router-view />
          </main>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <Footer :footerData="footerData">
            <template #logo>
              {{ SiteName }}
            </template>
          </Footer>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>
<style lang="scss" scoped>
*
{
  transition: all 0.3s ease;
}
</style>