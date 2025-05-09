<script lang="ts" setup>
defineProps<{
  members: {
    name: string;
    role: string;
    description: string;
    photo: string;
  }[];
}>();
</script>

<template>
  <v-container fluid class="pa-0">
    <v-row justify="center" align="stretch" class="my-8" dense>
      <v-col
          v-for="(member, index) in members"
          :key="index"
          cols="12"
          sm="6"
          lg="3"
          class="d-flex"
      >
        <v-card class="team-card elevation-4 w-100 d-flex flex-column" hover>
          <v-img
              :src="member.photo"
              class="team-image"
              cover
              alt="Zdjęcie członka zespołu"
          />

          <!-- Cała zawartość wypchnięta do dołu -->
          <div class="card-bottom pa-4 d-flex flex-column flex-grow-1">
            <div class="text-center mb-4">
              <h3 class="text-h6 font-weight-bold">{{ member.name }}</h3>
              <p class="text-subtitle-2 text-grey-darken-1 mb-2">{{ member.role }}</p>
              <p class="text-body-2 text-grey-darken-2">{{ member.description }}</p>
            </div>

            <div class="mt-auto">
              <v-divider class="w-50 mx-auto my-2" />
              <div class="d-flex justify-center ga-4">
                <v-icon color="grey-darken-1" size="20">mdi-twitter</v-icon>
                <v-icon color="grey-darken-1" size="20">mdi-instagram</v-icon>
                <v-icon color="grey-darken-1" size="20">mdi-linkedin</v-icon>
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.team-card {
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transition: border 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.team-image {
  aspect-ratio: 5/7;
  max-height: 60%;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  overflow: hidden;
  position: relative;
}
@media (max-width: 830px) {
  .team-image {
    max-height: 50%;
  }
}

/* Usunięcie efektu padding-bottom od Vuetify */
::v-deep(.team-image .v-responsive__sizer) {
  padding-bottom: 0 !important;
}

/* Dodatkowo: wymuszenie 100% wysokości na samym <img> */
::v-deep(.team-image .v-img__img) {
  height: 100% !important;
  object-fit: cover;
  object-position: top;
}
</style>

