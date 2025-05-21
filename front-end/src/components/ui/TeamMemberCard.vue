<script lang="ts" setup>
defineProps<{
  members: {
    name: string;
    role: string;
    description: string;
    photo: {
      src: string;
      alt: string;
    };
    github: string;
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
        <v-card class="team-card elevation-4 w-100 d-flex flex-column">
          <v-img
              :src="member.photo.src"
              class="team-image"
              cover
              :alt="member.photo.alt"
          />

          <div class="card-bottom pa-4 d-flex flex-column flex-grow-1 bottom-card">
            <div class="text-center mb-4">
              <h3 class="text-h6 font-weight-bold">{{ member.name }}</h3>
              <p class="text-subtitle-2 text-grey-darken-1 mb-2">{{ member.role }}</p>
              <p class="text-body-2 text-grey-darken-2">{{ member.description }}</p>
            </div>

            <div class="mt-auto">
              <v-divider class="w-80 mx-auto my-2" />
              <div class="d-flex justify-center ga-4">
                <a
                    :href="member.github"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                  <v-icon color="grey-darken-1" size="40" class="cursor-pointer">
                    mdi-github
                  </v-icon>
                </a>
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
  display: flex;
  height: 100%;
  flex-direction: column;
}
.team-image {
  aspect-ratio: 5/7;
  height: auto;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  overflow: hidden;
  position: relative;
}
.bottom-card{
  height: 60%;
}
</style>

