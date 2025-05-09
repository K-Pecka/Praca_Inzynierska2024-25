<script lang="ts" setup>
import { ref, onMounted } from "vue";

defineProps<{
  members: {
    name: string;
    role: string;
    description: string;
    photo?: string;
  }[];
}>();

const isSmallScreen = ref(false);

onMounted(() => {
  isSmallScreen.value = window.innerWidth <= 952;
});

window.addEventListener("resize", () => {
  isSmallScreen.value = window.innerWidth <= 952;
});
</script>

<template>
  <v-row
    class="d-flex ga-md-0 ga-8 my-5"
    :style="{
      margin: 'auto',
    }"
  >
  <v-carousel
    height="500"
    hide-delimiters
    show-arrows="hover"
    class="rounded-xl bg-grey-lighten-5 elevation-2"
    bg-color="transparent"
  >
    <v-carousel-item
      v-for="(member, index) in members"
      :key="index"
    >
      <v-container class="fill-height d-flex align-center">
        <v-row
          align="center"
          justify="center"
          class="w-100"
        >
          <!-- Awatar -->
          <v-col cols="12" md="4" class="d-flex justify-center mb-6 mb-md-0">
            <div
              v-if="member.photo"
              class="rounded-circle overflow-hidden elevation-4"
              style="width: 220px; height: 220px;"
            >
              <v-img
                :src="member.photo"
                cover
                alt="Zdjęcie członka zespołu"
              />
            </div>
          </v-col>

          <!-- Dane członka zespołu -->
          <v-col cols="12" md="6">
            <v-card
              class="pa-6 rounded-lg bg-white elevation-1"
              flat
            >
              <h3 class="text-h5 text-primary font-weight-bold mb-2">
                {{ member.name }}
              </h3>
              <p class="text-subtitle-1 text-grey-darken-1 font-italic mb-3">
                {{ member.role }}
              </p>
              <p class="text-body-1 text-grey-darken-3">
                {{ member.description }}
              </p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-carousel-item>
  </v-carousel>

  </v-row>
</template>

<style scoped>
.team-member-card {
  display: flex;
  flex-direction: row;
  border-radius: 16px;
  transition: transform 0.3s ease;
}

.team-avatar-wrapper {
  width: 120px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

.team-avatar-wrapper:hover {
  transform: scale(1.05);
}

.team-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.team-member-card:hover {
  transform: translateY(-5px);
}

@media (max-width: 600px) {
  .team-member-card {
    flex-direction: column;
  }

  .team-avatar-wrapper {
    margin: 0 auto;
  }
}
</style>
