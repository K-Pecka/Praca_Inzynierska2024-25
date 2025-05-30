<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { Section, Form, HeaderSection } from "@/components";
import {TermsDialog} from "@/components";
import { Register } from "@/types/interface";
import { FormType } from "@/types/enum";
import { useAuthStore, useFormStore, usePageHomeStore } from "@/stores";
const { getSectionTitle } = usePageHomeStore();
const { registerMutation } = useAuthStore();
const { initForm, sendForm, isFormValid } = useFormStore();

const sectionTitle = getSectionTitle(FormType.REGISTER);
const init = initForm(FormType.REGISTER);
const inputs = ref(init.inputs);
const formValues = ref(init.values);

const showTermsDialog = ref(false);
const afterAcceptCallback = ref<null | (() => void)>(null);

const TERMS_KEY = "hasAcceptedTerms";

const hasAcceptedTerms = ref(false);

onMounted(() => {
  hasAcceptedTerms.value = localStorage.getItem(TERMS_KEY) === "true";
});

const acceptRegulation = (
  fn: () => void,
  config: { validFn: typeof isFormValid }
) => {
  const isValid = config.validFn(FormType.REGISTER, formValues.value);
  if (!isValid) return;

  if (hasAcceptedTerms.value) {
    fn();
  } else {
    afterAcceptCallback.value = fn;
    showTermsDialog.value = true;
  }
};

const handleSubmit = async () => {
  await sendForm({
    data: formValues.value,
    send: async (data) => {
      const { pass_2, ...registrationData } = data;
      await registerMutation.mutateAsync(registrationData as Register);
    }
  });
};

const onAcceptTerms = () => {
  hasAcceptedTerms.value = true;
  localStorage.setItem(TERMS_KEY, "true");
  if (afterAcceptCallback.value) {
    afterAcceptCallback.value();
    afterAcceptCallback.value = null;
  }
};
</script>

<template>
  <Section class="logIn gradient-text">
    <template #title>
      <HeaderSection no-sub-title :title-gradient-text="sectionTitle" center />
    </template>

    <template #content>
      <Form
        :submitButtonLabel="sectionTitle"
        :inputs="inputs"
        :formValues="formValues"
        @submitForm="() =>
          acceptRegulation(handleSubmit, { validFn: isFormValid })"
      />
    </template>
    
  </Section>
  <TermsDialog
    v-model="showTermsDialog"
    title="Regulamin rejestracji"
    acceptButtonText="Akceptuję regulamin"
    :showCloseButton="true"
    @accepted="onAcceptTerms"
    @cancel="showTermsDialog = false"
  />
</template>
