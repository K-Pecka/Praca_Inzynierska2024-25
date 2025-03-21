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
              404
            </v-card-title>
            <v-card-subtitle class="text-h5 text--secondary">
              Podana strona nie istnieje
            </v-card-subtitle>
            <v-card-text>
              Coś poszło nie tak. Podana ścieżka nie istnieje.
            </v-card-text>
            <v-btn color="primary" @click="$router.push('/')">
              Wróć na stronę główną
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
  