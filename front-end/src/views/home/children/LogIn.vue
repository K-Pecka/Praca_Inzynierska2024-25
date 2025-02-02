<script lang="ts" setup>
import { ref } from "vue";
import Form from "@/components/Form.vue";
import Section from "@/components/Section.vue";
import { Validator } from "@/utils/validator/validation";
import { usePageStore } from "@/stores/pageContentStore";
import { useUserStore } from "@/stores/userStore";
import { computed } from "vue";
import ListLink from "@/components/ListLink.vue";
import { useRouter } from 'vue-router';
const router = useRouter();
const { getSectionTitle, errorMessage } = usePageStore();
const { login } = useUserStore();
const sectionTitle = getSectionTitle("login");

const validator = new Validator(errorMessage()).isEmpty().save();

const inputStyle = {
  color: "var(--primary-color)",
  fontSize: "2rem",
};

interface Input {
  name: string;
  label: string;
  type: string;
  placeholder: string;
  validation: Validator;
  error: string[];
}
const errorShow=ref(false);
const inputs = ref<Input[]>([
  {
    name: "email",
    label: "Podaj Email:",
    type: "text",
    placeholder: "Wprowadź email",
    validation: validator,
    error: [],
  },
  {
    name: "password",
    label: "Podaj Hasło:",
    type: "password",
    placeholder: "Wprowadź hasło",
    validation: validator,
    error: [],
  },
]);
const moreOption = [
  {
    label: "Zapomniałeś hasła?",
    href: "/",
  },
  {
    label: "Nie masz konta? Zarejestruj się.",
    href: "/register",
  },
];
const formValues = ref<Record<string, string>>(
  Object.fromEntries(inputs.value.map((input) => [input.name, ""]))
);
const validateForm = computed(() => {
  return inputs.value
    .map((input) => {
      const value = formValues.value[input.name];
      input.error = input.validation ? input.validation.validate(value) : [];
      return input.error.length === 0;
    })
    .every(Boolean);
});

const handleSubmit = async (_: any, config: any) => {
  if (config?.send && validateForm.value) {
    if(await login(formValues.value) == true)
    { 
      router.push('/panel');
    }else{
      errorShow.value=true;
    }
    console.log("Wartości formularza:");
    console.table(formValues.value);
  } else {
    // console.log("Wykryto błędy:");
    // const errorFields = inputs.value.map((input) => [
    //   input.name,
    //   ...input.error,
    // ]);
    // console.log(errorFields);
  }
};
</script>

<template>
  <Section class="logIn">
    <template #title>
      <h1 :style="inputStyle">{{ sectionTitle }}</h1>
    </template>
    <template #content>
      <Form
        :submitButtonLabel="sectionTitle"
        :inputs="inputs"
        :formValues="formValues"
        @submitForm="handleSubmit"
      >
        <template #moreOption v-if="moreOption.length > 0">
          <ListLink :links="moreOption" />
        </template>
        
      </Form>
      <span v-if="errorShow">Błędny login lub hasło.</span>
    </template>
  </Section>
</template>
<style lang="scss" scoped>
span{
  display: block;
  margin: auto;
  text-align: center;
  color:red;
}
</style>