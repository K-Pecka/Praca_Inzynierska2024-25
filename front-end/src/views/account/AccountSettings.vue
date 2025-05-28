<script setup lang="ts">
import {computed, ref} from 'vue';
import {Section, Form} from '@/components';
import {Input} from '@/types/interface';
import {useFormStore, useAuthStore} from '@/stores';
import {FormType} from "@/types/enum";

const { getFormInputs, isFormValid } = useFormStore();
const { updateProfileMutation, updatePasswordMutation ,getUser } = useAuthStore();
const personalInputs = ref<Input[]>(getFormInputs(FormType.PROFILE_PERSONAL));
const passwordInputs = ref<Input[]>(getFormInputs(FormType.PROFILE_PASSWORD));
const user = getUser();

const personalValues = ref<Record<string, string>>({
  first_name: user?.first_name ?? "",
  last_name: user?.last_name ?? "",
});

const passwordValues = ref<Record<string, string>>(
    Object.fromEntries(passwordInputs.value.map(i => [i.name, ""]))
);

const isChanged = computed(() => {
  return (
      personalValues.value.first_name !== (user?.first_name ?? "") ||
      personalValues.value.last_name !== (user?.last_name ?? "")
  );
});

const isPasswordValid = computed(() => {
  const newPass = passwordValues.value.new_pass;
  const repeatPass = passwordValues.value.repeat_pass;

  return (
      newPass.length >= 6 &&
      repeatPass.length >= 6 &&
      newPass === repeatPass
  );
});

async function handlePersonalSubmit(_: any, cfg: { send?: boolean }) {
  if (!cfg?.send || !isFormValid(FormType.PROFILE_PERSONAL, personalValues.value)) return;

  const { first_name, last_name } = personalValues.value;

  await updateProfileMutation.mutateAsync({ first_name, last_name });
}

async function handlePasswordSubmit(_: any, cfg: { send?: boolean }) {
  if (!cfg?.send || !isFormValid(FormType.PROFILE_PASSWORD, passwordValues.value)) {
    return;
  }
  const { new_pass, repeat_pass } = passwordValues.value;

  await updatePasswordMutation.mutateAsync({
    password: new_pass,
    password_confirm: repeat_pass,
  });
}
</script>

<template>
  <Section>
    <template #title>
      <h1 class="settings-title">Ustawienia konta</h1>
      <p class="settings-subtitle">Zaktualizuj swoje dane osobowe lub hasło</p>
    </template>

    <template #content>
      <Form
          :submitButtonLabel="'Zapisz dane osobowe'"
          :inputs="personalInputs"
          :formValues="personalValues"
          :disabled="!isChanged"
          @submitForm="handlePersonalSubmit"
      />
      <br />
      <Form
          :submitButtonLabel="'Zmień hasło'"
          :inputs="passwordInputs"
          :formValues="passwordValues"
          :disabled="!isPasswordValid"
          @submitForm="handlePasswordSubmit"
      />
    </template>
  </Section>
</template>

<style scoped lang="scss">
.settings-title {
  color: rgb(var(--v-theme-primary));
  font-size: 2rem;
}

.settings-subtitle {
  margin-bottom: .1rem;
  color: rgb(var(--v-theme-text), .8);
}
</style>