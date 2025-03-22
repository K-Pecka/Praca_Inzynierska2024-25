<script lang="ts" setup>
import {Form,ListLink,Section} from "@/components/common";
import { usePageHomeStore,useFormStore } from "@/stores/";
import { FormType } from "@/type/enum";

const { getSectionTitle } = usePageHomeStore();
const { getMoreOptions,initForm,sendForm, formValues } = useFormStore();

const sectionTitle = getSectionTitle(FormType.LOGIN);
const inputs = initForm(FormType.LOGIN);
const moreOptions = getMoreOptions();
const handleSubmit = async (formValue: any, config: any) => {
  sendForm(formValue, config);
};
</script>

<template>
  <Section class="logIn">
    <template #title>
      <h1>{{ sectionTitle }}</h1>
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
  color: rgb(var(--v-theme-primary));
  font-size: 2rem;
}
</style>
