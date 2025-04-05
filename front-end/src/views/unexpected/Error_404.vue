<script setup lang="ts">
import { useRoute } from "vue-router";
const route = useRoute();
import { computed,inject } from "vue";
const messages = inject('messages') as any;
const message =  route.query.message || messages.errorPage.error404.defaultMessage;
const code = route.query.code || messages.errorPage.error404.subtitle;
</script>
<template>
    <v-container class="error-container">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" md="8" class="text-center">
          <!-- <v-img
            src="/error_500.svg"
            height="400"
            class="animated-character"
          ></v-img> -->
          <v-card class="error-card">
            <v-card-title class="text-h2 text--primary">
              {{ messages.errorPage.error404.title }}
            </v-card-title>
            <v-card-subtitle class="text-h5 text--secondary">
              {{ code }}
            </v-card-subtitle>
            <v-card-text>
              {{ messages.errorPage.error404.discription }} {{ message }}
            </v-card-text>
            <v-btn color="primary" @click="$router.push('/')">
              {{ messages.errorPage.error404.button }}
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <style scoped>
  .error-container {
    background: rgb(var(--v-theme-surface));
    color: rgb(var(--v-theme-on-surface));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .error-card {
    background: rgb(var(--v-theme-background));
    color: rgb(var(--v-theme-on-background));
    padding: 20px;
    border-radius: 12px;
    box-shadow: rgb(var(--v-shadow-key-2));
  }
  
  </style>
  