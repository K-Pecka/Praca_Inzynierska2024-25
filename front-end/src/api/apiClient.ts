import axios from 'axios';
import { useAuthStore } from '@/stores/auth/useAuthStore';
import { apiEndpoints } from './apiEndpoints';
import { fetchRefreshToken } from './endpoints/auth';

const apiClient = axios.create({
    baseURL: 'https://api.plannder.com',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 5000,
});

// === KOLEJKA + FLAGA odświeżania ===
let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};

// === REQUEST INTERCEPTOR ===
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

// === RESPONSE INTERCEPTOR ===
apiClient.interceptors.response.use(
    response => response,
    async (error) => {
        const originalRequest = error.config;
        const authStore = useAuthStore();

        if (error.response?.status === 401 && !originalRequest._retry) {
            console.log('401 error', error.response?.data);
            const refreshToken = authStore.getToken()?.refresh;

            if (refreshToken && !isRefreshing) {
                originalRequest._retry = true;
                isRefreshing = true;

                try {
                    console.log('before', refreshToken);
                    const refreshResponse = await fetchRefreshToken(refreshToken);
                    console.log('after', refreshResponse);
                    const newAccess = refreshResponse;
                    authStore.saveToken(newAccess);
                    apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccess.access}`;
                    processQueue(null, newAccess);
                    return apiClient(originalRequest);
                } catch (refreshError) {
                    processQueue(refreshError, null);
                    authStore.logout();
                    return Promise.reject(refreshError);
                } finally {
                    isRefreshing = false;
                }
            }

            // Kolejka oczekujących
            return new Promise((resolve, reject) => {
                failedQueue.push({
                    resolve: (token: string) => {
                        originalRequest.headers['Authorization'] = `Bearer ${token}`;
                        resolve(apiClient(originalRequest));
                    },
                    reject: (err: any) => {
                        reject(err);
                    },
                });
            });
        }

        return Promise.reject(error);
    }
);

export default apiClient;
