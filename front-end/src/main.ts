import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "@/assets/style.scss";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import vuetify from "./lib/vuetify";
import { createPinia } from "pinia";
import { QueryClient, VueQueryPlugin } from "@tanstack/vue-query";
import "@mdi/font/css/materialdesignicons.css";
import piniaPersist from "pinia-plugin-persistedstate";
import { piniaBasePlugin } from "./plugins/piniaBase";
import { messages } from "./lib/messages";
const app = createApp(App);
const queryClient = new QueryClient({});

const pinia = createPinia();
pinia.use(piniaPersist);
pinia.use(piniaBasePlugin);

app.provide('messages', messages);

app
  .use(Toast)
  .use(pinia)
  .use(vuetify)
  .use(router)
  .use(VueQueryPlugin, { queryClient })
  .mount("#app");
