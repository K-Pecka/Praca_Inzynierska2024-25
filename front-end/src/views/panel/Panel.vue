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
              <router-view />
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>
