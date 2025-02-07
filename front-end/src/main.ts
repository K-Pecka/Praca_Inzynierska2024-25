import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@/assets/style.scss';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

const app = createApp(App);

import { createVuetify } from "vuetify";
import "vuetify/styles";

import { createPinia } from 'pinia';

const vuetify = createVuetify();

app.use(Toast).use(router).use(vuetify).use(createPinia()).mount('#app');