<template>
  <Section class="logIn">
    <template #title>
      <h1 :style="inputStyle">Logowanie</h1>
    </template>
    <template #content>
      <div class="container">
        <div class="form-container">
          <div class="wrapper">
            <form @submit.prevent="handleSubmit">
              <div v-for="(inputsData, index) in inputs" :key="index">
                <InputWithLabel
                  :inputData="inputsData"
                  v-model="formValues[inputsData.name]"
                />
              </div>
              <button type="submit">Zaloguj się</button>
            </form>
            <div class="extraOption">
              <div v-for="(option, index) in extraOption" :key="index">
                <a :href="option.href">{{ option.label }}</a>
              </div>
            </div>
          </div>
        </div>

        <div class="more-action">
          <Btn v-for="(option, index) in moreOption" :key="index">
            <template #icon>
              <img src="@/assets/vue.svg" />
            </template>
            <template #text>
              {{ option.text }}
            </template>
          </Btn>
        </div>
      </div>
    </template>
  </Section>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import InputWithLabel from "@/components/InputWithLabel.vue";
import Section from "@/components/Section.vue";
import Btn from "@/components/Btn.vue";
const inputStyle = {
  color: "var(--primary-color)",
  fontSize: "2rem",
};
const moreOption = [
  { icon: "@/assets/vue.svg" },
  { icon: "@/assets/vue.svg", text: "Zaloguj się za pomocą Google" },
];
const inputs = ref([
  {
    name: "email",
    label: "Podaj Email:",
    type: "email",
    placeholder: "Wprowadź email",
  },
  {
    name: "password",
    label: "Podaj Hasło:",
    type: "password",
    placeholder: "Wprowadź hasło",
  },
]);
const extraOption = [
  { label: "Zapomniałeś hasła?", href: "/" },
  { label: "Nie masz konta? Zarejestruj się.", href: "/" },
];
const formValues = ref<Record<string, string>>(
  Object.fromEntries(inputs.value.map((input) => [input.name, ""]))
);

const handleSubmit = () => {
  console.log("Wartości formularza:", formValues.value);
};
</script>

<style scoped>
.container {
  width: 50%;
  margin: auto;
}
.form-container {
  width: 100%;
  background-color: rgba(var(--rgb-secondary-color), 0.9);
  margin: auto;
  padding: 0.25rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
}
.extraOption a {
  color: var(--text-color);
}
.extraOption div {
  margin: 2rem auto;
}
.wrapper {
  padding-left: 2rem;
  padding-right: 2rem;
}
button {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: auto;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  border: none;
  padding: 1rem;
  cursor: pointer;
}
</style>
