<script lang="ts" setup>
import {Form, HeaderSection, ListLink, Section} from "@/components/common";
import { usePageHomeStore,useFormStore } from "@/stores/";
import { FormType } from "@/types/enum";
import { ref } from "vue";

const { getSectionTitle } = usePageHomeStore();
const { getMoreOptions,initForm,sendForm, formValues } = useFormStore();

const sectionTitle = getSectionTitle(FormType.LOGIN);
const inputs = ref(initForm(FormType.LOGIN));
const moreOptions = getMoreOptions();
const handleSubmit = async (formValue: any, config: any) => {
  sendForm(formValue, config);
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
