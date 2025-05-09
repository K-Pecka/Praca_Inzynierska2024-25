<script setup lang="ts">
import { ref, computed } from 'vue';
import Section from '@/components/common/Section.vue';
import AppButton from '@/components/AppButton.vue';
import { useNotificationStore } from '@/stores';
import {HeaderSection} from "@/components";

const { setSuccessCurrentMessage, setErrorCurrentMessage } = useNotificationStore();

const form = ref({
  name: '',
  email: '',
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
          title="Skontaktuj się z nami"
          subtitle="Masz pytania? Skontaktuj się z nami – chętnie pomożemy."
          center
      />
    </template>

    <template #content>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="4">
            <h3>Dane kontaktowe</h3>
            <p><v-icon start size="20">mdi-email-outline</v-icon> plannder@gmail.com</p>
            <p><v-icon start size="20">mdi-phone-outline</v-icon> +48&nbsp;123&nbsp;456&nbsp;789</p>
            <p><v-icon start size="20">mdi-map-marker-outline</v-icon> Gdańsk, ul.&nbsp;Gdańska&nbsp;1</p>
          </v-col>

          <v-col cols="12" md="6">
            <v-form validate-on="blur lazy" @submit.prevent="handleSubmit">
              <v-text-field
                  v-model="form.name"
                  :rules="nameRules"
                  label="Imię"
                  variant="outlined"
                  required
                  bg-color="background"
                  density="comfortable"
              />
              <v-text-field
                  v-model="form.email"
                  :rules="emailRules"
                  label="E‑mail"
                  type="email"
                  variant="outlined"
                  required
                  bg-color="background"
                  density="comfortable"
              />
              <v-textarea
                  v-model="form.message"
                  :rules="messageRules"
                  label="Wiadomość"
                  variant="outlined"
                  rows="4"
                  required
                  bg-color="background"
                  density="comfortable"
              />
              <AppButton
                  color="primary"
                  type="submit"
                  max-width="120px"
                  class="mt-4 font-weight-bold"
                  :disabled="!isFormValid"
                  text="Wyślij"
              />
            </v-form>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </Section>
</template>
