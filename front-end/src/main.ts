import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@/assets/style.scss';

const app = createApp(App);

import { createVuetify } from "vuetify";
import "vuetify/styles";

const vuetify = createVuetify();

app.use(router).use(vuetify).mount('#app');