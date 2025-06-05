<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import HeaderSection from "@/components/shared/HeaderSection.vue";
import AppButton from "@/components/AppButton.vue";
import { useAuthStore, useUtilsStore } from "@/stores";

const name = ref("");
const surname = ref("");
const password = ref("");
const confirmPassword = ref("");
const formRef = ref();

const nameRules = [(v: string) => !!v || "Imię jest wymagane"];
const surnameRules = [(v: string) => !!v || "Nazwisko jest wymagane"];
const passwordRules = [
  (v: string) => !!v || "Hasło jest wymagane",
  (v: string) => v.length >= 8 || "Hasło musi mieć co najmniej 8 znaków",
  (v: string) =>
    /[a-z]/.test(v) || "Hasło musi zawierać co najmniej jedną małą literę",
  (v: string) =>
    /[A-Z]/.test(v) || "Hasło musi zawierać co najmniej jedną wielką literę",
  (v: string) =>
    /\d/.test(v) || "Hasło musi zawierać co najmniej jedną cyfrę",
  (v: string) =>
    /[!@#$%^&*(),.?":{}|<>_\-\\/~`+=\[\]]/.test(v) ||
    "Hasło musi zawierać znak specjalny",
];
const confirmPasswordRules = [
  (v: string) => !!v || "Powtórz hasło",
  (v: string) => v === password.value || "Hasła muszą się zgadzać",
];
const { saveToken, userUpdateMutation } = useAuthStore();

async function goToLogin() {
  const result = await formRef.value?.validate();
  console.log("TAK");
  console.log(result)
    if (result?.valid && confirmPassword.value === password.value) {
      console.log("TAK2");
      userUpdateMutation.mutate({
        first_name: name.value,
        last_name: surname.value,
        password: password.value,
        password_confirm: confirmPassword.value,
      });
    };
}

onMounted(() => {
  const route = useRoute();
  const { validToken } = useUtilsStore();
  const token = String(route.query.token);
  if (validToken(token, "initialAccessToken")) {
    saveToken({ initialAccessToken: token });
  }
});
</script>

<template>
  <v-container
    class="fill-height d-flex flex-column align-center justify-center"
  >
    <v-card max-width="700" class="pa-8 rounded-lg">
      <v-card-title class="text-left">
        <HeaderSection
          title="Dołącz do"
          title-gradient-text="wycieczki!"
          no-sub-title
        />
      </v-card-title>

      <v-card-text class="mt-4 text-left">
        Zostałeś zaproszony do wspólnej podróży. Uzupełnij dane, aby
        kontynuować.

        <v-form ref="formRef" class="mt-6" validate-on="blur">
          <v-row dense class="mb-3" align="stretch">
            <v-col cols="12" md="6">
              <v-text-field
                v-model="name"
                label="Imię"
                :rules="nameRules"
                variant="outlined"
                density="comfortable"
                rounded="md"
                required
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="surname"
                label="Nazwisko"
                :rules="surnameRules"
                variant="outlined"
                density="comfortable"
                rounded="md"
                required
              />
            </v-col>
          </v-row>

          <v-text-field
            v-model="password"
            label="Hasło"
            type="password"
            :rules="passwordRules"
            variant="outlined"
            density="comfortable"
            rounded="md"
            class="mb-4"
            required
          />

          <v-text-field
            v-model="confirmPassword"
            label="Powtórz hasło"
            type="password"
            :rules="confirmPasswordRules"
            variant="outlined"
            density="comfortable"
            rounded="md"
            required
          />
        </v-form>
      </v-card-text>

      <v-card-actions class="justify-center mt-6">
        <AppButton
          color="primary"
          @click="goToLogin"
          dense
          font-auto
          max-width="100%"
          text="Dołącz teraz"
        />
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>
