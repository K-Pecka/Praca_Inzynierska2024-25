<script setup lang="ts">
import {ref, computed} from 'vue';
import Section from '@/components/common/Section.vue';
import AppButton from '@/components/AppButton.vue';
import {useNotificationStore} from '@/stores';
import {HeaderSection} from "@/components";

const {setSuccessCurrentMessage, setErrorCurrentMessage} = useNotificationStore();

const form = ref({
  name: '',
  email: '',
  title: '',
  message: '',
});

const emailRegex = /^[\w-.]+@([\w-]+\.)+[\w-]{2,}$/;
const isEmailValid = (email: string) => emailRegex.test(email);

const isFormValid = computed(() =>
    form.value.name.trim() !== '' &&
    form.value.message.trim() !== '' &&
    isEmailValid(form.value.email)
);

const nameRules = [(v: string) => !!v || 'Imię jest wymagane'];
const emailRules = [
  (v: string) => !!v || 'E‑mail jest wymagany',
  (v: string) => isEmailValid(v) || 'Niepoprawny adres e‑mail',
];
const messageRules = [(v: string) => !!v || 'Wiadomość nie może być pusta'];


function handleSubmit() {
  if (!isFormValid.value) {
    setErrorCurrentMessage('Uzupełnij poprawnie wszystkie pola, aby wysłać wiadomość.');
    return;
  }
  setSuccessCurrentMessage('Dziękujemy za wiadomość! Odpiszemy najszybciej jak to możliwe.');
}
</script>

<template>
  <Section class="pb-10">
    <template #title>
      <HeaderSection
          title="Get In"
          title-gradient-text="Touch"
          subtitle="Gotowy na zbudowanie niesamowitej współpracy z naszą aplikacją? Zostaw nam wiadomość i odezwiemy się do Ciebie."
          center
      />
    </template>

    <template #content>
      <v-row justify="center">

        <!-- Left v-card -->
        <v-col cols="12" lg="6">
          <v-card rounded="lg" class="h-100">
            <v-card-text>
              <v-form validate-on="blur lazy" @submit.prevent="handleSubmit" class="pa-4">

                <!-- Name input -->
                <v-text-field
                    v-model="form.name"
                    :rules="nameRules"
                    label="Twoje imię"
                    variant="outlined"
                    required
                    bg-color="background"
                    base-color="blue-grey-lighten-3"
                    rounded="lg"
                    density="comfortable"
                />

                <!-- Email input -->
                <v-text-field
                    v-model="form.email"
                    :rules="emailRules"
                    label="Twój e‑mail"
                    type="email"
                    variant="outlined"
                    required
                    bg-color="background"
                    base-color="blue-grey-lighten-3"
                    rounded="lg"
                    density="comfortable"
                />

                <!-- Subject input -->
                <v-text-field
                    v-model="form.title"
                    :rules="messageRules"
                    label="Temat"
                    variant="outlined"
                    required
                    bg-color="background"
                    base-color="blue-grey-lighten-3"
                    rounded="lg"
                    density="comfortable"
                />

                <!-- Text input -->
                <v-textarea
                    v-model="form.message"
                    :rules="messageRules"
                    label="Wiadomość"
                    variant="outlined"
                    rows="4"
                    required
                    bg-color="background"
                    base-color="blue-grey-lighten-3"
                    rounded="lg"
                    density="comfortable"
                />

                <!-- Send button -->
                <AppButton
                    color="primary"
                    type="submit"
                    max-width="120px"
                    min-height="50px"
                    class="mt-4 font-weight-bold"
                    icon
                    rounded="lg"
                    text="Wyślij"
                />
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Right v-card -->
        <v-col cols="12" lg="6">
          <v-card rounded="lg" class="h-100">
            <v-card-text>

              <!-- email card -->
              <v-row
                  class="contact-item rounded-lg mx-1 mx-lg-8 mx-md-8 px-7 py-2 mt-1 mb-4"
                  justify="center"
              >
                <v-col cols="auto" lg="1">
                  <v-row
                      justify="center"
                      no-gutters
                      class="pr-0 pr-md-4 pr-lg-4"
                  >
                  <span class="rounded-lg contact-accent-bg">
                    <v-icon size="23px" class="contact-icon">
                      mdi-email-outline
                    </v-icon>
                  </span>
                  </v-row>
                </v-col>
                <v-col v-if="$vuetify.display.width > 650">
                  <v-row
                      class="flex-column"
                      justify="start"
                      align="start"
                      no-gutters
                  >
                    <span class="text-h5 contact-title mb-2">
                      Wyślij nam maila
                    </span>

                    <span class="text-h6 color-text mb-1 contact-content">
                    Odpowiemy w ciągu 24 godzin
                    </span>

                    <span class="text-h6 contact-accent-color mb-1 contact-footer">
                      plannder@kontakt.com
                    </span>
                  </v-row>
                </v-col>
              </v-row>

              <!-- Phone card -->
              <v-row
                  class="contact-item rounded-lg mx-1 mx-lg-8 mx-md-8 px-7 py-2 mt-1 mb-4"
                  justify="center"
              >
                <v-col
                    cols="auto"
                    lg="1"
                >
                  <v-row
                      justify="center"
                      no-gutters
                      class="pr-0 pr-md-4 pr-lg-4"
                  >
                  <span class="rounded-lg contact-orange-bg">
                    <v-icon
                        size="23px"
                        class="contact-icon"
                    >
                      mdi-phone-outline
                    </v-icon>
                  </span>
                  </v-row>
                </v-col>
                <v-col v-if="$vuetify.display.width > 650">
                  <v-row
                      class="flex-column"
                      justify="start"
                      align="start"
                      no-gutters
                  >
                  <span class="text-h5 contact-title mb-2">
                    Zadzwoń do nas
                  </span>
                    <span class="text-h6 color-text mb-1 contact-content">
                    Pon-Pt od 9:00 do 18:00
                  </span>
                    <span class="text-h6 contact-accent-color mb-1 contact-footer">
                      +48 883 777 767
                    </span>
                  </v-row>
                </v-col>
              </v-row>

              <!-- localisation card -->
              <v-row
                  class="contact-item rounded-lg mx-1 mx-lg-8 mx-md-8 px-7 py-2 mt-1 mb-4"
                  justify="center"
              >
                <v-col cols="auto" lg="1">
                  <v-row
                      justify="center"
                      no-gutters
                      class="pr-0 pr-md-4 pr-lg-4"
                  >
                  <span class="rounded-lg contact-cyan-bg">
                    <v-icon size="23px" class="contact-icon">
                      mdi-map-marker-outline
                    </v-icon>
                  </span>
                  </v-row>
                </v-col>
                <v-col v-if="$vuetify.display.width > 650">
                  <v-row
                      class="flex-column"
                      justify="start"
                      align="start"
                      no-gutters
                  >
                  <span class="text-h5 contact-title mb-2">
                    Odwiedź nas
                  </span>
                    <span class="text-h6 color-text mb-1 contact-content">
                      Przywitaj się z nami osobiście w naszym biurze
                    </span>
                    <span class="text-h6 contact-accent-color mb-1 contact-footer">
                    Targ drzewny 14, Gdańsk, PL
                  </span>
                  </v-row>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </Section>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.contact-item {
  border: 1px solid rgb(0, 0, 0, 0.04);
}

.contact-icon {
  margin: 10px;
  color: white;
}

.contact-content {
  line-height: 0.9;
}

.contact-footer {
  word-break: break-word;
}

.contact-title {
  font-weight: 600;
}

.contact-accent-bg {
  background-color: #B39DDB;
}

.contact-orange-bg {
  background-color: #F57F17;
}

.contact-cyan-bg {
  background-color: #4DD0E1;
}

.contact-accent-color {
  color: #B39DDB;
}

:deep(.v-field-label) {
  color: black;
  opacity: 1;
  font-weight: 600;
}
</style>