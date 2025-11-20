import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export async function login(email, password) {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);
  params.append("grant_type", "password");

  const res = await api.post("/api/auth/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  return res.data;
}

export async function getCurrentUser() {
  const res = await api.get("/api/users/me");
  return res.data;
}

export default api;
