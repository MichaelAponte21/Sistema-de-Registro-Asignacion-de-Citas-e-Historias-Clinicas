// src/api/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Interceptor para adjuntar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export async function login(email, password) {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);
  formData.append("username", email);
  formData.append("password", password);
  formData.append("grant_type", "password");

  axios.post("http://localhost:8000/api/auth/token", formData);

  const res = await api.post("/api/auth/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  return res.data;
}

// Obtener info del usuario y su rol
export async function getCurrentUser() {
  const res = await api.get("/api/users/me");
  return res.data;
}

export default api;
