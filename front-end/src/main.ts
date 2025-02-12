import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@/assets/style.scss';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import vuetify from './lib/vuetify';
import { createPinia } from 'pinia';
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query';
import '@mdi/font/css/materialdesignicons.css';
const app = createApp(App);

const queryClient = new QueryClient();

app.use(Toast)
   .use(router)
   .use(vuetify)
   .use(createPinia())
   .use(VueQueryPlugin, { queryClient })
   .mount('#app');
