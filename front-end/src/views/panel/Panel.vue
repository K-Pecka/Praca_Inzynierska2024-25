<script lang="ts" setup>
import { ref } from "vue";

const form = ref({
  email: "",
  password: "",
});
</script>
<template>
  <v-app>
    <v-container>
      <v-row>
        <v-col>
          <v-card>
            <v-card-title>
              <h1>Panel</h1>
            </v-card-title>
            <v-card-text> hej </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>
