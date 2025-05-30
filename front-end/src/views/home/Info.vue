registration-failed<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router'
const router = useRouter()
const ComunicationType = {
    'registration-failed':{description:"Wystąpił błąd w czasie rejestracji",status:"delete",router:{name:'landing'},icon:"mdi-close-circle"}
}
const props = defineProps<{ type: keyof typeof ComunicationType }>()
const comunication = computed(()=>ComunicationType[props.type])
console.log(comunication)
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
      <v-icon :color="comunication.status" size="56" class="mb-4">{{ comunication.icon}}</v-icon>

      <h2 class="text-h5 font-weight-medium mb-2">
        {{comunication.description}}
      </h2>

      <v-btn :color="comunication.status" variant="flat" @click="router.push(comunication.router)">
        Powrót
      </v-btn>
    </v-card>
  </v-container>
</template>
