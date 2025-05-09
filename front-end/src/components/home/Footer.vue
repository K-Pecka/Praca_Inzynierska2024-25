<script setup>
  import { useDisplay } from 'vuetify'
  import { images } from "@/data/index.ts";

  const { smAndDown } = useDisplay()

  const links = [
    'Oferta',
    'O nas',
    'Kontakt',
  ]
</script>

<template>
  <v-footer class="d-flex align-center justify-center ga-2 flex-wrap flex-grow-1 py-3 footer">
    <v-col
        cols="8"
        class="d-flex flex-column"
    >
      <!-- Top section -->
      <v-row
          class="pb-5"
          :class="{ 'justify-center': smAndDown, 'justify-space-between': !smAndDown }"
          align="end"

      >
        <!-- Logo -->
        <v-img
            class="pb-3"
            aspect-ratio="16/9"
            :src="images.logo.img"
            :min-width="100"
            :max-width="150"
            v-if="!smAndDown"
        />

        <!-- Buttons -->
        <div>
          <v-btn
            v-for="link in links"
            :key="link"
            :text="link"
            variant="plain"
            :ripple="false"
            rounded
            class="pr-0 pl-8"
          />
        </div>
      </v-row>

      <!-- Bottom section -->
      <v-row>
        <v-divider class="pb-5" thickness="2" />
        <div class="flex-1-0-100 text-center mt-2">
          {{ new Date().getFullYear() }} — <strong>Plannder</strong>
        </div>
      </v-row>
    </v-col>
  </v-footer>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.footer {
  background-color: rgb($secondary-color);
  min-height: $footer-height;
}
</style>
