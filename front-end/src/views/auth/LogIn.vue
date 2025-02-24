<script lang="ts" setup>
import Form from "@/components/common/Form.vue";
import ListLink from "@/components/ListLink.vue";
import Section from "@/components/Section.vue";

import { usePageHomeStore,useFormStore } from "@/stores/";
import { FormType } from "@/type/enum";

const { getSectionTitle } = usePageHomeStore();
const { getMoreOptions,initForm,sendForm, formValues } = useFormStore();

const sectionTitle = getSectionTitle(FormType.LOGIN);
const inputs = initForm(FormType.LOGIN);
const moreOptions = getMoreOptions();

const handleSubmit = async (_: any, config: any) => {
  sendForm(_, config);
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
