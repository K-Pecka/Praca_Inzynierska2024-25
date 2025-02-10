import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@/assets/style.scss';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import vuetify from './lib/vuetify';
import { createPinia } from 'pinia';

const app = createApp(App);

app.use(Toast).use(router).use(vuetify).use(createPinia()).mount('#app');