import axios from "axios";
import { useAuthStore } from "@/stores/auth/useAuthStore";
import { fetchRefreshToken } from "./endpoints/auth";
import router from "@/router";
import { useUtilsStore } from "@/stores";

const apiClient = axios.create({
  baseURL: "https://api.plannder.com",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 5000,
});

let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
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
    const { validToken } = useUtilsStore();
    const token = authStore.getToken();
    if (token) {
      const { initialAccessToken, access } = token;

      if (
        initialAccessToken &&
        validToken(initialAccessToken, "initialAccessToken")
      ) {
        config.headers.set("Authorization", `Bearer ${initialAccessToken}`);
      } else if (access && validToken(access, "access")) {
        config.headers.set("Authorization", `Bearer ${access}`);
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// === RESPONSE INTERCEPTOR ===
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const authStore = useAuthStore();
    if (error.response?.status === 404) {
      // router.push('/404');
    }
    if (error.response?.status === 500) {
      router.push("/500");
    } else if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      authStore.getToken()?.access != undefined
    ) {
      const refreshToken = authStore.getToken()?.refresh;
      if (refreshToken && !isRefreshing) {
        originalRequest._retry = true;
        isRefreshing = true;
        try {
          const refreshResponse = await fetchRefreshToken(refreshToken);
          const newAccess = refreshResponse;
          authStore.saveToken(newAccess);
          apiClient.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${newAccess.access}`;
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

      return new Promise((resolve, reject) => {
        failedQueue.push({
          resolve: (token: string) => {
            originalRequest.headers["Authorization"] = `Bearer ${token}`;
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
