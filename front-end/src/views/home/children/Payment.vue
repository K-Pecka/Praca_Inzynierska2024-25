<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <v-container
    class="d-flex justify-center align-center"
    style="min-height: 90vh"
    fluid
  >
    <v-card
      class="pa-8 d-flex flex-column align-center text-center"
      max-width="420"
      elevation="2"
      style="border-radius: 20px; background-color: #f5fdfb;"
    >
      <v-icon color="success" size="56" class="mb-4">mdi-check-circle</v-icon>

      <h2 class="text-h5 font-weight-medium mb-2">
        Płatność zakończona sukcesem
      </h2>

      <p class="text-body-2 text-grey-darken-1 mb-6">
        Dziękujemy za dokonanie płatności. Potwierdzenie zostało wysłane na Twój adres e-mail.
      </p>

      <v-btn color="success" variant="flat" @click="router.push({name:'logOut'})">
        Powrót
      </v-btn>
    </v-card>
  </v-container>
</template>
