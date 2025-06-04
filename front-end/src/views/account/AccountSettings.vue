<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Section, Form } from "@/components";
import { Input } from "@/types/interface";
import { useFormStore, useAuthStore } from "@/stores";
import { FormType } from "@/types/enum";
import { AppCard } from "@/components";
const { getFormInputs, isFormValid } = useFormStore();
const { updateProfileMutation, updatePasswordMutation, userData } =
  useAuthStore();
const personalInputs = ref<Input[]>(getFormInputs(FormType.PROFILE_PERSONAL));
const passwordInputs = ref<Input[]>(getFormInputs(FormType.PROFILE_PASSWORD));
const user = userData.getUser();
import { useSafeDelete } from "@/composables/useSafeDelete";
const { confirmAndRun } = useSafeDelete();

const cancelSubscription = () => {
  confirmAndRun(
    () => {
      useAuthStore().cancelSubscription.mutate();
    },
    {
      title: "Potwierdź anulowanie subskrybcji",
      message:
        "Czy na pewno chcesz przerwać subskrybcję? Tego działania nie można cofnąć.",
      wordToConfirm: "ZGODA",
    }
  );
};
const deleteUser = () =>{
  confirmAndRun(
    () => {
      useAuthStore().deleteUser.mutate();
    },
    {
      title: "Potwierdź usunięcie konta",
      message:
        "Czy na pewno chcesz usunąć swoje konto? Tej operacji nie można cofnąć. Wszystkie utworzone przez Ciebie dane zostaną trwale i nieodwracalnie usunięte.",
      wordToConfirm: "TAK, CHCĘ USUNĄĆ",
    }
  );
}
const personalValues = ref<Record<string, string>>({
  first_name: user?.first_name ?? "",
  last_name: user?.last_name ?? "",
});

const passwordValues = ref<Record<string, string>>(
  Object.fromEntries(passwordInputs.value.map((i) => [i.name, ""]))
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
    newPass.length >= 6 && repeatPass.length >= 6 && newPass === repeatPass
  );
});

async function handlePersonalSubmit(_: any, cfg: { send?: boolean }) {
  if (
    !cfg?.send ||
    !isFormValid(FormType.PROFILE_PERSONAL, personalValues.value)
  )
    return;

  const { first_name, last_name } = personalValues.value;

  await updateProfileMutation.mutateAsync({ first_name, last_name });
}

async function handlePasswordSubmit(_: any, cfg: { send?: boolean }) {
  if (
    !cfg?.send ||
    !isFormValid(FormType.PROFILE_PASSWORD, passwordValues.value)
  ) {
    return;
  }
  const { new_pass, repeat_pass } = passwordValues.value;

  await updatePasswordMutation.mutateAsync({
    password: new_pass,
    password_confirm: repeat_pass,
  });
}
type SubscriptionPlan = "free" | "tourist" | "guide" | "cancel";
const SubscriptionTypeCommunication: Record<SubscriptionPlan, string> = {
  free: "Nie posiadasz jeszcze żadnej subskrypcji",
  tourist:
    "Twoja subskrypcja turysty pozostaje aktywna do końca bieżącego okresu rozliczeniowego.",
  guide:
    "Twoja subskrypcja przewodnika pozostaje aktywna do końca bieżącego okresu rozliczeniowego.",
  cancel: "Towja subskrypcja wygaśnie wraz z końcem okresu rozliczeniowego",
};
const cancel = ref(user?.subscription_cancelled);
const plan: SubscriptionPlan =
  (user?.subscription_plan as SubscriptionPlan) ?? "free";
const subscription = ref(
  !user?.subscription_cancelled
    ? SubscriptionTypeCommunication[plan]
    : SubscriptionTypeCommunication["cancel"]
);
watch(
  () => userData.getUser(),
  (newUser) => {
    if (newUser?.subscription_cancelled) {
      subscription.value =
        "Towja subskrypcja wygaśnie wraz z końcem okresu rozliczeniowego";
        cancel.value = true
    }
  }
);
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
      <v-col cols="12" md="6" lg="8" offset-md="3" offset-lg="2" noPadding>
        <AppCard noPadding>
          <v-card class="mb-6" elevation="0" color="transparent">
            <v-card-title class="text-h6 d-flex align-center">
              <v-icon icon="mdi-credit-card-outline" class="" />
              Zarządzanie subskrypcją
            </v-card-title>
            <v-card-text>
              <p class="mb-4">
                <strong class="pl-1">Uwaga:</strong>{{ subscription }}
              </p>
              <v-btn
                color="warning"
                prepend-icon="mdi-cancel"
                rounded
                variant="flat"
                :disabled="cancel || !user?.subscription_active"
                @click="cancelSubscription"
              >
                Anuluj subskrypcję
              </v-btn>
            </v-card-text>
          </v-card>
          <v-card class="red-lighten-5" elevation="0" color="transparent">
            <v-card-title class="text-h6 text-red-darken-2 d-flex align-center">
              <v-icon icon="mdi-account-remove-outline" class="mr-2" />
              Usuwanie konta
            </v-card-title>
            <v-card-text>
              <p class="mb-4">
                <strong>Uwaga:</strong> Usunięcie konta jest nieodwracalne.
                Wszystkie dane zostaną bezpowrotnie utracone.
              </p>
              <v-btn
                color="red-darken-2"
                prepend-icon="mdi-delete-alert"
                rounded
                variant="flat"
                @click="deleteUser"
              >
                Usuń konto
              </v-btn>
            </v-card-text>
          </v-card>
        </AppCard>
      </v-col>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.settings-title {
  color: rgb(var(--v-theme-primary));
  font-size: 2rem;
}

.settings-subtitle {
  margin-bottom: 0.1rem;
  color: rgb(var(--v-theme-text), 0.8);
}
</style>
