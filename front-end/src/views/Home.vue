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
          Plannder
          <!--img src="@/assets/vue.svg" alt="Hero image" /-->
        </template>
      </Footer>
  
    </div>
  </template>
  
  <script lang="ts" setup>
  import Navbar from "@/components/Navbar.vue";
  import Footer from "@/components/Footer.vue";
  const navLinksBase = [
  { label: "Oferta", href: "/" },
  { label: "Kontakt", href: "/" },
];
const user = false;
const navLinks = [
  ...navLinksBase,
  ...(user
    ? [{ label: "Panel", href: "/", active: true }]
    : [
        { label: "Zaloguj się", href: "/logIn" },
        { label: "Zarejestruj się", href: "/", active: true },
      ]),
];
  const footerData = {
    links: [
      { label: "Oferta", href: "/" },
      { label: "Kontakt", href: "/" },
      { label: "Panel", href: "/" },
    ],
    footerText: "© 2024 Plannder Wszystkie prawa zastrzeżone",
  };
  </script>
  
  