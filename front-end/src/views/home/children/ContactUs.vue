<script setup lang="ts">
import { ref } from 'vue';
import Section from '@/components/common/Section.vue';
import AppButton from '@/components/budget/AppButton.vue';
import { useNotificationStore } from '@/stores';

const { setSuccessCurrentMessage } = useNotificationStore();

const form = ref({
  name: '',
  email: '',
  message: '',
});

function handleSubmit() {
  setSuccessCurrentMessage('Dziękujemy za wiadomość! Odpiszemy najszybciej jak to możliwe.');
  console.log({name: '', email: '', message: ''});
}
</script>

<template>
  <Section>
    <template #title>
      <h1 class="contact-title">Skontaktuj się z nami</h1>
      <p class="contact-subtitle">
        Masz pytania? Skontaktuj się z nami – chętnie pomożemy.
      </p>
    </template>

    <template #content>
      <v-container class="contact-container" fluid>
        <v-row>
          <v-col cols="12" md="6" class="mb-6 mb-md-0">
            <h3 class="contact-heading">Dane kontaktowe</h3>
            <p><v-icon start size="20">mdi-email-outline</v-icon> kontakt.plannder@gmail.com</p>
            <p><v-icon start size="20">mdi-phone-outline</v-icon> +48&nbsp;123&nbsp;456&nbsp;789</p>
            <p><v-icon start size="20">mdi-map-marker-outline</v-icon> Gdańsk, ul.&nbsp;Gdańska&nbsp;1</p>
          </v-col>

          <v-col cols="12" md="6">
            <v-form validate-on="blur lazy" @submit.prevent="handleSubmit" class="form-wrapper">
              <v-text-field
                  v-model="form.name"
                  label="Imię"
                  variant="outlined"
                  required
                  bg-color="background"
                  density="comfortable"
              />
              <v-text-field
                  v-model="form.email"
                  label="E‑mail"
                  type="email"
                  variant="outlined"
                  required
                  bg-color="background"
                  density="comfortable"
              />
              <v-textarea
                  v-model="form.message"
                  label="Wiadomość"
                  variant="outlined"
                  rows="4"
                  required
                  bg-color="background"
                  density="comfortable"
              />
              <AppButton size="md" variant="primary" type="submit" class="mt-4">Wyślij</AppButton>
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
  font-size: 2.25rem;
  font-weight: 700;
  margin-bottom: .25rem;
}
.contact-subtitle {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: rgb(var(--v-theme-text), .8);
}
.contact-heading {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.contact-container p {
  font-size: 1rem;
  margin: .5rem 0;
  display: flex;
  align-items: center;
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
}
</style>
