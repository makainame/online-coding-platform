import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const isAuthRequest = String(error.config?.url || "").includes("/auth/");
    if (error.response?.status === 401 && !isAuthRequest) {
      localStorage.removeItem("token");
      window.location.assign("/");
    }
    return Promise.reject(error);
  }
);

window.addEventListener("unhandledrejection", (event) => {
  const isAuthRequest = String(event.reason?.config?.url || "").includes("/auth/");
  if (event.reason?.response?.status === 401 && !isAuthRequest) {
    event.preventDefault();
  }
});

export default api;
