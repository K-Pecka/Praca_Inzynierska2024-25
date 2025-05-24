<script lang="ts" setup>
import { Form, HeaderSection, ListLink, Section } from "@/components/common";
import { usePageHomeStore, useFormStore, useAuthStore } from "@/stores/";
import { FormType } from "@/types/enum";
import { ref } from "vue";

const { getSectionTitle } = usePageHomeStore();
const { getMoreOptions, initForm, sendForm } = useFormStore();
const { loginMutation } = useAuthStore();
const sectionTitle = getSectionTitle(FormType.LOGIN);
const init = initForm(FormType.LOGIN);
const inputs = ref(init.inputs);
const formValues = ref(init.values);
const moreOptions = getMoreOptions();

const handleSubmit = async () => {
  await sendForm({
    data: formValues.value,
    send: async (data: Record<string, string>) => {
      await loginMutation.mutateAsync(data);
    }
  });
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
        @submitForm="handleSubmit"
      >
        <template #moreOption v-if="moreOptions.length > 0">
          <ListLink :links="moreOptions" />
        </template>
      </Form>
    </template>
  </Section>
</template>

<style lang="scss" scoped>
h1 {
  font-size: 2rem;
}
</style>
