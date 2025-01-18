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
                  <span v-if="errors[inputsData.name]" class="error-message">
                    {{ errors[inputsData.name] }}
                  </span>
                </div>
                <button type="submit">Zarejestruj się</button>
              </form>
              <div class="extraOption" v-if="config.extraOption">
                <div v-for="(option, index) in extraOption" :key="index">
                  <a :href="option.href">{{ option.label }}</a>
                </div>
              </div>
            </div>
          </div>
  
          <div class="more-action" v-if="config.moreAction">
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

  const config = {
    extraOption: false,
    moreAction: false,
  };
  
  const inputStyle = {
    color: "var(--primary-color)",
    fontSize: "2rem",
  };
  
  const moreOption = [
    { icon: "@/assets/vue.svg", text: "Zaloguj się za pomocą Google" },
  ];
  const isEmpty = (value: string): boolean => value.trim() === '';

  const inputs = ref([
    { name: "name", label: "Podaj Imie:", type: "text", placeholder: "Wprowadź imie",onInput:isEmpty,errorMessage:"Pole musi być uzupełnione." },
    { name: "surname", label: "Podaj Nazwisko:", type: "text", placeholder: "Wprowadź nazwisko",onInput:isEmpty },
    { name: "email", label: "Podaj e-mail:", type: "email", placeholder: "Wprowadź e-mail",onInput:isEmpty },
    { name: "pass_1", label: "Podaj hasło:", type: "password", placeholder: "Wprowadź hasło",onInput:isEmpty },
    { name: "pass_2", label: "Podaj ponownie hasło:", type: "password", placeholder: "Wprowadź hasło",onInput:isEmpty }
  ]);

  const extraOption = [
    { label: "Zapomniałeś hasła?", href: "/" },
    { label: "Nie masz konta? Zarejestruj się.", href: "/" }
  ];
  
  const formValues = ref<Record<string, string>>(Object.fromEntries(inputs.value.map(input => [input.name, ""])));
  const errors = ref<Record<string, string>>({});

  
  const handleSubmit = () => {
      console.log("Wartości formularza:", formValues.value);
  };
  </script>
  
  <style scoped lang="scss">
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
    padding: 2rem;
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
  .more-action {
    img {
      width: 1.5rem;
      height: 1.5rem;
      padding: 0.25rem;
    }
  }
  
  .error-message {
    color: red;
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
  </style>
  