import axios from 'axios';
import { useAuthStore } from '@/stores/auth/useAuthStore';

const apiClient = axios.create({
    baseURL: 'https://api.plannder.com',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 5000,
});

apiClient.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore();
        const token = authStore.getToken()?.access;

        if (token) {
            config.headers.set('Authorization', `Bearer ${token}`);
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default apiClient;