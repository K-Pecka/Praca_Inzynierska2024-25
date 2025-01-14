import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@/assets/style.scss';

const app = createApp(App);

app.config.globalProperties.$siteName = import.meta.env.VITE_APP_SITE_NAME;

app.use(router).mount('#app');