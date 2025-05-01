<script setup lang="ts">
import { ref, computed } from 'vue';
import Section from '@/components/common/Section.vue';
import AppButton from '@/components/budget/AppButton.vue';
import { useNotificationStore } from '@/stores';

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
  console.log(form.value);
}
</script>

<template>
  <Section class="py-10">
    <template #title>
      <h1 class="contact-title text-h4 text-center text-primary font-weight-bold mb-6">Skontaktuj się z nami</h1>
      <p class="contact-subtitle">
        Masz pytania? Skontaktuj się z nami – chętnie pomożemy.
      </p>
    </template>

    <template #content>
      <v-container class="contact-container">
        <v-row justify="center">
          <v-col cols="12" md="4">
            <h3 class="contact-heading">Dane kontaktowe</h3>
            <p><v-icon start size="20">mdi-email-outline</v-icon> plannder@gmail.com</p>
            <p><v-icon start size="20">mdi-phone-outline</v-icon> +48&nbsp;123&nbsp;456&nbsp;789</p>
            <p><v-icon start size="20">mdi-map-marker-outline</v-icon> Gdańsk, ul.&nbsp;Gdańska&nbsp;1</p>
          </v-col>

          <v-col cols="12" md="6">
            <v-form validate-on="blur lazy" @submit.prevent="handleSubmit" class="form-wrapper">
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
              <AppButton size="md" variant="primary" type="submit" class="mt-4" :disabled="!isFormValid">Wyślij</AppButton>
            </v-form>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.contact-title {
  color: rgb(var(--v-theme-primary));
  margin-bottom: .1rem;
}

.contact-subtitle {
  margin-bottom: 1.5rem;
  color: rgb(var(--v-theme-text), .8);
}
.contact-heading {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.contact-container {
  font-size: 1rem;
  margin: .5rem 0;
  gap: .25rem;
}
.form-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (max-width: 380px) {
  .contact-title {
    font-size: 1.75rem;
  }
  .contact-subtitle {
    font-size: 1.5rem;
  }
  .contact-heading {
    font-size: 1.1rem;
  }
  .contact-container {
    font-size: .8rem;
  }
  .form-wrapper {
    gap: .5rem;
  }
}

</style>
