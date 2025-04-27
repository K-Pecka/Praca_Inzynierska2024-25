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
    class="d-flex ga-md-0 ga-8"
    :style="{
      'max-width': $vuetify.display.lgAndUp ? '80%' : '100%',
      margin: 'auto',
    }"
  >
    <v-col
      v-for="(member, index) in members"
      :key="member.name"
      cols="12"
      sm="10"
      offset-sm="1"
      offset-md="0"
      md="6"
      class="d-flex"
    >
      <v-card
        class="team-member-card w-100"
        elevation="4"
        color="primary"
        variant="tonal"
      >
        <v-row
          class="d-flex align-center pa-4"
          :class="{
            'flex-row-reverse':
              member?.photo && isSmallScreen && index % 2 === 1,
          }"
        >
          <v-col
            v-if="member.photo"
            cols="12"
            sm="4"
            class="d-flex justify-center"
          >
            <div class="team-avatar-wrapper">
              <v-img
                :src="member.photo"
                alt="Zdjęcie członka zespołu"
                class="team-avatar"
                aspect-ratio="1"
                cover
              />
            </div>
          </v-col>

          <v-col cols="12" :class="member.photo ? 'sm:col-span-8' : 'sm:col-span-12'">
            <v-card-text>
              <h3
                class="font-weight-bold"
                :class="{
                  'text-body-1': !$vuetify.display.smAndUp,
                  'text-h6': $vuetify.display.smAndUp,
                }"
              >
                {{ member.name }}
              </h3>
              <p class="text-subtitle-1 font-italic">{{ member.role }}</p>
              <p class="text-body-1">{{ member.description }}</p>
            </v-card-text>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
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
