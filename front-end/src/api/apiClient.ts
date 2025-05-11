import axios from 'axios';
import { useAuthStore } from '@/stores';

const apiClient = axios.create({
    baseURL: 'https://api.plannder.com',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 5000,
});

apiClient.interceptors.request.use((config) => {
    const { getToken } = useAuthStore();
    const token = getToken()?.access;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default apiClient;