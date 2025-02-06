<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import Form from "@/components/Form.vue";
import ListLink from "@/components/ListLink.vue";
import Section from "@/components/Section.vue";

import { usePageStore } from "@/stores/pageContentStore";
import { useUserStore } from "@/stores/userStore";
import { useFormStore } from "@/stores/formStore";
import { useMessageStore } from "@/stores/messageStore";
import {FormType,Input} from "@/type/interface";

const router = useRouter();

const { getSectionTitle } = usePageStore();
const { login } = useUserStore();
const { getFormInputs, validateForm, getMoreOptions } = useFormStore();
const { loginError } = useMessageStore();

const sectionTitle = getSectionTitle(FormType.LOGIN);
const inputs = ref<Input[]>(getFormInputs(FormType.LOGIN));

const formValues = ref<Record<string, string>>(
  Object.fromEntries(inputs.value.map((input: { name: string; }) => [input.name, ""]))
);

const errorShow = ref(false);
const moreOptions = ref(getMoreOptions());

const handleSubmit = async (_: any, config: any) => {
  if (config?.send && validateForm(FormType.LOGIN, formValues.value)) {
    const isLoggedIn = await login(formValues.value);
    if (isLoggedIn) {
      router.push("/panel");
    } else {
      errorShow.value = true;
    }
  }
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
      <span v-if="errorShow">{{ loginError() }}</span>
    </template>
  </Section>
</template>

<style lang="scss" scoped>
h1 {
  color: var(--primary-color);
  font-size: 2rem;
}

span {
  display: block;
  margin: auto;
  text-align: center;
  color: red;
}
</style>
