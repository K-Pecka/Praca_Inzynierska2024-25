<script setup lang="ts">
import {ref} from 'vue';
import {Section, Form} from '@/components';
import {Input} from '@/type/interface';
import {useFormStore} from '@/stores';
import {FormType} from '@/type/enum';
import {useAuthStore} from '@/stores';

const {getFormInputs, isFormValid} = useFormStore();
const {updateProfileMutation} = useAuthStore();

const inputs = ref<Input[]>(getFormInputs(FormType.PROFILE));
const formValues = ref<Record<string, string>>(
    Object.fromEntries(inputs.value.map(i => [i.name, '']))
);

async function handleSubmit(_: any, cfg: { send?: boolean }) {
  if (!cfg?.send) return;
  if (!isFormValid(FormType.PROFILE, formValues.value)) return;

  const {firstName, lastName, currentPass, newPass} = formValues.value;
  const payload = {
    first_name: firstName,
    last_name: lastName,
    current_password: currentPass,
    new_password: newPass,
  };
  try {
    await updateProfileMutation.mutateAsync(payload);
  } catch {
  }
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
          :submitButtonLabel="'Zapisz zmiany'"
          :inputs="inputs"
          :formValues="formValues"
          @submitForm="handleSubmit"
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
  margin-bottom: 1rem;
  color: rgb(var(--v-theme-text), .8);
}
</style>