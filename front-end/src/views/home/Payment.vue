<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router'
const router = useRouter()
const props = defineProps<{ status: string }>()
const success = computed(()=>props.status == 'success')
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
      <v-icon :color="success ? 'success' : 'delete'" size="56" class="mb-4">{{ props.status === 'success' ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>

      <h2 class="text-h5 font-weight-medium mb-2">
        {{success ? 'Płatność zakończona sukcesem' : 'Błąd płatności' }}
      </h2>

      <p class="text-body-2 text-grey-darken-1 mb-6">
        {{
          success
            ? 'Dziękujemy za dokonanie płatności. Potwierdzenie zostało wysłane na Twój adres e-mail.'
            : 'Wystąpił problem z płatnością. Za chwilę nastąpi przekierowanie na stronę główną.'
        }}
      </p>

      <v-btn v-if="success" color="success" variant="flat" @click="router.push({name:'logOut'})">
        Powrót
      </v-btn>
      <v-btn v-else color="delete" variant="flat" @click="router.push({name:'landing'})">
        Powrót
      </v-btn>
    </v-card>
  </v-container>
</template>
