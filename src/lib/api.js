import axios from "axios";

// In dev we proxy through Vite; in prod we need the real URL
const baseURL = import.meta.env.DEV
  ? "/api"
  : import.meta.env.VITE_API_URL?.replace(/\/$/, "") || "/api";

export const api = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

// Attach the token from localStorage to every non-auth request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  const url = config.url ?? "";
  const isAuthRoute = /\/(login|register)$/.test(url);

  if (token && !isAuthRoute) {
    config.headers = { ...config.headers, Authorization: `Bearer ${token}` };
  }

  return config;
});

// Pull a readable message out of whatever the API throws at us
export function getApiError(err, fallback = "Something went wrong. Please try again.") {
  const body = err?.response?.data;

  if (body) {
    if (typeof body === "string") return body;
    return body.message || body.error || JSON.stringify(body);
  }

  if (err?.code === "ERR_NETWORK") {
    return "Can't reach the server. Make sure the backend is running and the Vite proxy is pointing at the right port.";
  }

  return err?.message || fallback;
}
