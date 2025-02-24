<script setup lang="ts">
import { ref } from "vue";
import TicketUploader from "@/components/trip/TicketUploader.vue";

const selectedFile = ref<File | null>(null);

function handleFile(file: File) {
  selectedFile.value = file;

}
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12" md="10" offset-md="1">
        <v-card class="pa-4">
          <v-card-title>
            <h2>Dodaj Bilet</h2>
          </v-card-title>
          <v-card-text>
            <TicketUploader @file-selected="handleFile" />
            <div v-if="selectedFile" class="mt-4">
              <strong>Wybrano plik:</strong> {{ selectedFile.name }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss">

</style>