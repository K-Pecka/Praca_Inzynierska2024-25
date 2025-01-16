<script lang="ts" setup>
import Navbar from "@/components/main/Navbar.vue";
import Footer from "@/components/main/Footer.vue";

const SiteName=import.meta.env.VITE_APP_SITE_NAME;

const navLinksBase = [
  { label: "Oferta", href: "/",className:["navbar__link--base"] },
  { label: "O nas", href: "/" ,className:["navbar__link--base"]},
  { label: "Kontakt", href: "/",className:["navbar__link--base"] },
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
  links: [
    ...navLinksBase,
    { label: "Panel", href: "/" },
  ],
  footerText: `© 2025 Plannder Wszystkie prawa zastrzeżone `,
  subSection: `ostatnia modyfikacja: ${new Date().toLocaleDateString()}`
};
</script>

<template>
  <div class="app">
    <Navbar :links="navLinks">
      <template #logo>
        <img src="@/assets/vue.svg" alt="App Logo" />
      </template>
    </Navbar>

    <main>
      <router-view />
    </main>

    <Footer :footerData="footerData">
      <template #logo>
        {{ SiteName }}
      </template>
    </Footer>
  </div>
</template>
